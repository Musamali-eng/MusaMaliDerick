"""
Assignment 2: File Organization Automation
File: file_organizer_automation.py

A comprehensive file organization tool with real-time monitoring capabilities.
Organizes files in a directory by their type/extension into categorized folders.
"""

import json
import logging
import os
import shutil
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

# Optional watchdog import for monitoring
try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    Observer = None
    FileSystemEventHandler = object

# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_organizer.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Configuration - WITH frozen=True and helper methods
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Config:
    """
    Configuration settings for the file organizer.
    
    Attributes:
        source_dir: Directory to organize files from
        destination_dir: Directory to move organized files to (defaults to source)
        dry_run: If True, preview changes without moving files
        extension_map: Custom extension to category mappings
        ignore_extensions: File extensions to ignore
        ignore_patterns: Filename patterns to ignore
        auto_organize: Automatically organize new files
        watch_interval: Seconds between scans when watching
    """
    source_dir: Path
    destination_dir: Optional[Path] = None
    dry_run: bool = True
    extension_map: Dict[str, str] = field(default_factory=dict)
    ignore_extensions: Set[str] = field(default_factory=set)
    ignore_patterns: List[str] = field(default_factory=list)
    auto_organize: bool = False
    watch_interval: int = 5

    def __post_init__(self) -> None:
        """Initialize default values after dataclass creation."""
        if self.destination_dir is None:
            object.__setattr__(self, 'destination_dir', self.source_dir)

        if not self.ignore_extensions:
            object.__setattr__(self, 'ignore_extensions', {
                '.tmp', '.temp', '.cache', '.lock', '.ini', '.log'
            })

        if not self.ignore_patterns:
            object.__setattr__(self, 'ignore_patterns', [
                'desktop.ini', 'thumbs.db', '.DS_Store'
            ])

    def with_dry_run(self, dry_run: bool) -> 'Config':
        """
        Create a new config with the dry_run setting changed.
        
        Args:
            dry_run: New dry_run value (True = preview, False = actually move)
            
        Returns:
            New Config instance with updated dry_run setting
        """
        return Config(
            source_dir=self.source_dir,
            destination_dir=self.destination_dir,
            dry_run=dry_run,
            extension_map=self.extension_map,
            ignore_extensions=self.ignore_extensions,
            ignore_patterns=self.ignore_patterns,
            auto_organize=self.auto_organize,
            watch_interval=self.watch_interval
        )

    def with_source_dir(self, source_dir: Path) -> 'Config':
        """
        Create a new config with a different source directory.
        
        Args:
            source_dir: New source directory path
            
        Returns:
            New Config instance with updated source directory
        """
        return Config(
            source_dir=source_dir,
            destination_dir=self.destination_dir,
            dry_run=self.dry_run,
            extension_map=self.extension_map,
            ignore_extensions=self.ignore_extensions,
            ignore_patterns=self.ignore_patterns,
            auto_organize=self.auto_organize,
            watch_interval=self.watch_interval
        )

    @classmethod
    def from_json(cls, json_path: Path) -> 'Config':
        """Load configuration from a JSON file."""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return cls(
            source_dir=Path(data.get('source_dir', Path.home() / 'Downloads')),
            destination_dir=Path(data.get('destination_dir', Path.home() / 'Downloads')),
            dry_run=data.get('dry_run', True),
            extension_map=data.get('extension_map', {}),
            ignore_extensions=set(data.get('ignore_extensions', [])),
            ignore_patterns=data.get('ignore_patterns', []),
            auto_organize=data.get('auto_organize', False),
            watch_interval=data.get('watch_interval', 5)
        )

    def to_json(self, json_path: Path) -> None:
        """Save configuration to a JSON file."""
        data = {
            'source_dir': str(self.source_dir),
            'destination_dir': str(self.destination_dir),
            'dry_run': self.dry_run,
            'extension_map': self.extension_map,
            'ignore_extensions': list(self.ignore_extensions),
            'ignore_patterns': self.ignore_patterns,
            'auto_organize': self.auto_organize,
            'watch_interval': self.watch_interval
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)


# -----------------------------------------------------------------------------
# File Organizer
# -----------------------------------------------------------------------------

class FileOrganizer:
    """
    Main file organizer that categorizes and moves files.
    
    Features:
        - Categorizes files by extension and filename patterns
        - Handles duplicate files with timestamp renaming
        - Supports dry-run mode for preview
        - Provides statistics and logging
    """
    
    # Default file type categories with extensions
    DEFAULT_CATEGORIES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp',
                   '.tiff', '.tif', '.ico', '.heic', '.raw', '.psd', '.ai'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx',
                      '.ppt', '.pptx', '.md', '.rtf', '.odt', '.ods', '.odp',
                      '.csv', '.xml', '.yaml', '.yml', '.toml'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz',
                     '.iso', '.tgz', '.tbz2', '.zst'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
                   '.m4v', '.mpg', '.mpeg', '.3gp', '.ogv'],
        'Music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a',
                  '.aiff', '.wv', '.opus'],
        'Code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.go',
                 '.rs', '.json', '.xml', '.sh', '.bat', '.ps1', '.sql',
                 '.ts', '.jsx', '.tsx', '.vue', '.php', '.rb', '.pl',
                 '.lua', '.r', '.swift', '.kt', '.dart'],
        'Executables': ['.exe', '.msi', '.dmg', '.app', '.deb', '.rpm',
                        '.pkg', '.apk', '.bin', '.run'],
        'Subtitles': ['.srt', '.sub', '.ass', '.ssa', '.vtt'],
        'Design': ['.psd', '.ai', '.sketch', '.xd', '.fig'],
        'Fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
    }
    
    # Fallback filename patterns for files without extensions
    PATTERN_MAPPINGS = {
        'Videos': ['s01', 's1', 'episode', '720p', '1080p', '2160p', 'h264', 'h265', 'x264', 'x265'],
        'Music': ['track', 'album', 'remix', 'feat', 'ft.'],
        'Documents': ['report', 'summary', 'notes', 'letter', 'invoice'],
    }

    def __init__(self, config: Config) -> None:
        """
        Initialize the file organizer with configuration.
        
        Args:
            config: Configuration object with settings
        """
        self.config = config
        self.stats: Dict[str, int] = {
            'moved': 0,
            'skipped': 0,
            'errors': 0,
            'duplicates': 0,
            'processed': 0
        }
        
        # Build category map
        self.categories = self._build_category_map()
    
    def _build_category_map(self) -> Dict[str, List[str]]:
        """Build the category map with custom extensions."""
        categories = self.DEFAULT_CATEGORIES.copy()
        
        # Apply custom mappings
        for ext, category in self.config.extension_map.items():
            ext = ext if ext.startswith('.') else f'.{ext}'
            if category in categories:
                if ext not in categories[category]:
                    categories[category].append(ext)
            else:
                categories[category] = [ext]
        
        return categories

    def get_target_category(self, file_path: Path) -> str:
        """
        Determine the target category for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Category name or 'IGNORED' if file should be skipped
        """
        # Check if file should be ignored
        if self._should_ignore(file_path):
            return 'IGNORED'
        
        # Check by extension
        extension = file_path.suffix.lower()
        for category, extensions in self.categories.items():
            if extension in extensions:
                return category
        
        # Fallback: check filename patterns for files without extensions
        filename = file_path.name.lower()
        for category, patterns in self.PATTERN_MAPPINGS.items():
            if any(pattern in filename for pattern in patterns):
                return category
        
        return 'Other'

    def _should_ignore(self, file_path: Path) -> bool:
        """Check if a file should be ignored."""
        filename = file_path.name.lower()
        
        # Check ignore patterns
        if any(pattern.lower() in filename for pattern in self.config.ignore_patterns):
            return True
        
        # Check ignore extensions
        if file_path.suffix.lower() in self.config.ignore_extensions:
            return True
        
        return False

    def _get_destination_path(self, file_path: Path, category: str) -> Path:
        """
        Get the destination path for a file, handling duplicates.
        
        Args:
            file_path: Source file path
            category: Target category
            
        Returns:
            Destination path (with timestamp if duplicate exists)
        """
        dest_dir = self.config.destination_dir / category
        dest_path = dest_dir / file_path.name
        
        # Handle duplicates with timestamp
        if dest_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stem = file_path.stem
            suffix = file_path.suffix
            dest_path = dest_dir / f"{stem}_{timestamp}{suffix}"
            self.stats['duplicates'] += 1
        
        return dest_path

    def organize(self) -> Dict[str, int]:
        """
        Organize all files in the source directory.
        
        Returns:
            Dictionary with organization statistics
        """
        source_dir = self.config.source_dir
        dest_base = self.config.destination_dir
        dry_run = self.config.dry_run
        
        # Validate source directory
        if not source_dir.exists():
            logger.error(f"Directory {source_dir} does not exist")
            return self.stats
        
        # Log start
        mode = 'DRY RUN' if dry_run else 'ORGANIZING'
        logger.info(f"[{mode}] - {'Simulation' if dry_run else 'Actual Move'}")
        logger.info(f"Source: {source_dir}")
        logger.info(f"Destination: {dest_base}")
        logger.info("-" * 60)
        
        # Reset statistics
        self.stats = {k: 0 for k in self.stats}
        
        # Create destination directories
        if not dry_run:
            for category in self.categories:
                (dest_base / category).mkdir(exist_ok=True)
        
        # Process files
        files = [f for f in source_dir.iterdir() if f.is_file()]
        total = len(files)
        
        for idx, file_path in enumerate(files, 1):
            self.stats['processed'] += 1
            
            # Show progress for large folders
            if total > 50 and idx % 10 == 0:
                logger.info(f"Progress: {idx}/{total} files")
            
            # Check if file should be ignored
            if self._should_ignore(file_path):
                logger.debug(f"Skipped (ignored): {file_path.name}")
                self.stats['skipped'] += 1
                continue
            
            try:
                # Get target category
                category = self.get_target_category(file_path)
                if category == 'IGNORED':
                    self.stats['skipped'] += 1
                    continue
                
                # Get destination path
                dest_path = self._get_destination_path(file_path, category)
                
                # Move or simulate
                if dry_run:
                    logger.info(f"Would move: {file_path.name} -> {category}/")
                    self.stats['moved'] += 1
                else:
                    shutil.move(str(file_path), str(dest_path))
                    self.stats['moved'] += 1
                    logger.info(f"Moved: {file_path.name} -> {category}/")
                    
            except Exception as e:
                self.stats['errors'] += 1
                logger.error(f"Error moving {file_path.name}: {e}")
        
        # Log summary
        self._log_summary()
        return self.stats

    def _log_summary(self) -> None:
        """Log the organization summary."""
        logger.info("-" * 60)
        logger.info("Organization Summary:")
        logger.info(f"  Files processed: {self.stats['processed']}")
        logger.info(f"  Files moved: {self.stats['moved']}")
        logger.info(f"  Skipped: {self.stats['skipped']}")
        logger.info(f"  Duplicates: {self.stats['duplicates']}")
        logger.info(f"  Errors: {self.stats['errors']}")
        logger.info(f"  Mode: {'DRY RUN (no changes made)' if self.config.dry_run else 'COMPLETED'}")

    def get_stats(self) -> Dict:
        """
        Get statistics about files in the source directory.
        
        Returns:
            Dictionary with file statistics
        """
        source_dir = self.config.source_dir
        
        if not source_dir.exists():
            return {'error': 'Directory does not exist'}
        
        stats = {
            'total_files': 0,
            'total_size': 0,
            'categories': {},
            'file_types': {},
        }
        
        for file_path in source_dir.iterdir():
            if file_path.is_file():
                stats['total_files'] += 1
                stats['total_size'] += file_path.stat().st_size
                
                category = self.get_target_category(file_path)
                stats['categories'][category] = stats['categories'].get(category, 0) + 1
                
                ext = file_path.suffix.lower() or 'no_extension'
                stats['file_types'][ext] = stats['file_types'].get(ext, 0) + 1
        
        # Add human-readable sizes
        stats['total_size_mb'] = stats['total_size'] / (1024 * 1024)
        stats['total_size_gb'] = stats['total_size'] / (1024 * 1024 * 1024)
        
        return stats


# -----------------------------------------------------------------------------
# Folder Monitoring
# -----------------------------------------------------------------------------

if WATCHDOG_AVAILABLE:
    class FolderMonitor(FileSystemEventHandler):
        """Monitor a folder and trigger organization on new files."""
        
        def __init__(self, organizer: FileOrganizer, delay: int = 2) -> None:
            self.organizer = organizer
            self.delay = delay
            self.last_organize = 0
        
        def on_created(self, event) -> None:
            """Handle file creation events."""
            if not event.is_directory:
                logger.info(f"New file detected: {event.src_path}")
                time.sleep(self.delay)
                
                # Rate limit to avoid multiple triggers
                current = time.time()
                if current - self.last_organize > self.organizer.config.watch_interval:
                    self.last_organize = current
                    self.organizer.organize()


def watch_folder(organizer: FileOrganizer) -> None:
    """Watch a folder and organize files automatically."""
    if not WATCHDOG_AVAILABLE:
        logger.error("Watchdog not installed. Install with: pip install watchdog")
        return
    
    event_handler = FolderMonitor(organizer)
    observer = Observer()
    observer.schedule(event_handler, str(organizer.config.source_dir), recursive=False)
    observer.start()
    
    logger.info(f"Watching {organizer.config.source_dir} for new files...")
    logger.info("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Stopped watching")
    observer.join()


# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------

def get_config_path() -> Path:
    """Get the default configuration file path."""
    return Path.home() / ".file_organizer_config.json"


def load_or_create_config() -> Config:
    """Load configuration from file or create default."""
    config_path = get_config_path()
    
    if config_path.exists():
        logger.info(f"Loading config from: {config_path}")
        return Config.from_json(config_path)
    
    logger.info("Creating default config...")
    config = Config(
        source_dir=Path.home() / "Downloads",
        destination_dir=Path.home() / "Downloads",
        dry_run=True,
        extension_map={
            '.torrent': 'Archives',
            '.log': 'Documents',
            '.csv': 'Documents',
            '.psd': 'Design',
            '.ai': 'Design',
            '.epub': 'Documents',
            '.mobi': 'Documents',
            '.apk': 'Executables',
            '.dmg': 'Executables',
            '.pkg': 'Executables',
            '.ttf': 'Fonts',
            '.otf': 'Fonts',
            '.srt': 'Subtitles',
            '.ass': 'Subtitles',
        },
        ignore_extensions={'.tmp', '.temp', '.cache', '.lock'},
        ignore_patterns=['desktop.ini', 'thumbs.db', '.DS_Store'],
        auto_organize=False,
        watch_interval=5
    )
    config.to_json(config_path)
    logger.info(f"Default config saved to: {config_path}")
    return config


def quick_organize() -> None:
    """Quick one-shot organization with default settings."""
    config = Config(
        source_dir=Path.home() / "Downloads",
        dry_run=False
    )
    organizer = FileOrganizer(config)
    organizer.organize()


# -----------------------------------------------------------------------------
# Interactive Interface
# -----------------------------------------------------------------------------

def print_header(text: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"[{text}]")
    print("=" * 60)


def interactive_mode() -> None:
    """Run the interactive command-line interface."""
    config = load_or_create_config()
    
    while True:
        print_header("FILE ORGANIZER AUTOMATION")
        print("1. Show file statistics")
        print("2. Organize files (dry run)")
        print("3. Organize files (actual move)")
        print("4. Watch folder for changes")
        print("5. Edit configuration")
        print("6. Save current configuration")
        print("7. Quick organize (use defaults)")
        print("8. Exit")
        print("-" * 60)
        
        choice = input("Select option (1-8): ").strip()
        
        if choice == '1':
            organizer = FileOrganizer(config)
            stats = organizer.get_stats()
            print("\nFile Statistics:")
            print(f"  Total files: {stats.get('total_files', 0)}")
            print(f"  Total size: {stats.get('total_size_mb', 0):.2f} MB "
                  f"({stats.get('total_size_gb', 0):.2f} GB)")
            if 'categories' in stats and stats['categories']:
                print("\n  Categories:")
                for cat, count in sorted(stats['categories'].items(), key=lambda x: -x[1]):
                    print(f"    {cat}: {count} files")
        
        elif choice == '2':
            # Use with_dry_run() to create a new config with dry_run=True
            dry_config = config.with_dry_run(True)
            organizer = FileOrganizer(dry_config)
            organizer.organize()
        
        elif choice == '3':
            # Use with_dry_run() to create a new config with dry_run=False
            confirm = input("WARNING: This will ACTUALLY MOVE files. Continue? (yes/no): ")
            if confirm.lower() in ['yes', 'y']:
                move_config = config.with_dry_run(False)
                organizer = FileOrganizer(move_config)
                organizer.organize()
            else:
                print("Operation cancelled")
        
        elif choice == '4':
            # Use with_dry_run() for watch mode
            watch_config = config.with_dry_run(False)
            organizer = FileOrganizer(watch_config)
            print("\nStarting folder watch mode...")
            watch_folder(organizer)
        
        elif choice == '5':
            config_path = get_config_path()
            print(f"\nEdit configuration file: {config_path}")
            print("The file will open in your default editor...")
            
            # Open in default editor
            import platform
            import subprocess
            if platform.system() == 'Windows':
                os.startfile(config_path)
            elif platform.system() == 'Darwin':
                subprocess.call(['open', config_path])
            else:
                subprocess.call(['xdg-open', config_path])
            
            input("Press Enter after editing...")
            config = load_or_create_config()
            print("Configuration reloaded")
        
        elif choice == '6':
            config_path = get_config_path()
            config.to_json(config_path)
            print(f"Configuration saved to {config_path}")
        
        elif choice == '7':
            quick_organize()
        
        elif choice == '8':
            print("Goodbye!")
            break
        
        else:
            print("Invalid option. Please select 1-8.")


# -----------------------------------------------------------------------------
# Main Entry Point
# -----------------------------------------------------------------------------

def main() -> None:
    """Main entry point for the script."""
    try:
        # Command-line mode
        if len(sys.argv) > 1:
            config = load_or_create_config()
            command = sys.argv[1]
            
            if command == '--organize':
                # Create new config with dry_run=False
                organize_config = config.with_dry_run(False)
                organizer = FileOrganizer(organize_config)
                organizer.organize()
            elif command == '--dry-run':
                # Create new config with dry_run=True
                dry_config = config.with_dry_run(True)
                organizer = FileOrganizer(dry_config)
                organizer.organize()
            elif command == '--watch':
                # Create new config for watch mode
                watch_config = config.with_dry_run(False)
                organizer = FileOrganizer(watch_config)
                watch_folder(organizer)
            elif command == '--stats':
                organizer = FileOrganizer(config)
                stats = organizer.get_stats()
                print(json.dumps(stats, indent=2))
            elif command == '--quick':
                quick_organize()
            else:
                print("Usage:")
                print("  python file_organizer.py --organize   # Actually move files")
                print("  python file_organizer.py --dry-run    # Preview changes")
                print("  python file_organizer.py --watch      # Monitor folder")
                print("  python file_organizer.py --stats      # Show statistics")
                print("  python file_organizer.py --quick      # Quick organize")
                print("  python file_organizer.py              # Interactive mode")
        else:
            # Interactive mode
            interactive_mode()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()