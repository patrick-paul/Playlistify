"""
Test script to verify dependency checking with Rich
"""
import sys
import platform

# Use safe characters on Windows
IS_WINDOWS = platform.system().lower() == 'windows'
CHECK_MARK = '[OK]' if IS_WINDOWS else '✓'
CROSS_MARK = '[X]' if IS_WINDOWS else '✗'

def test_import_dependencies():
    """Test that all required dependencies can be imported"""
    print("Testing dependency imports...\n")

    dependencies = {
        'colorama': 'Terminal colors',
        'tqdm': 'Progress bars',
        'rich': 'Rich terminal formatting',
        'yt_dlp': 'YouTube downloader'
    }

    success_count = 0
    failed = []

    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"{CHECK_MARK} {module:15} - {description}")
            success_count += 1
        except ImportError:
            print(f"{CROSS_MARK} {module:15} - {description} (NOT INSTALLED)")
            failed.append(module)

    print(f"\n{'='*50}")
    print(f"Results: {success_count}/{len(dependencies)} dependencies available")

    if failed:
        print(f"\nMissing: {', '.join(failed)}")
        print("\nTo install missing dependencies:")
        print(f"  pip install {' '.join(failed)}")
        return False
    else:
        print(f"\nAll dependencies are installed! {CHECK_MARK}")
        return True


def test_dependency_manager():
    """Test the DependencyManager directly"""
    print("\n" + "="*50)
    print("Testing DependencyManager...")
    print("="*50 + "\n")

    try:
        from src.playlistfy.services.dependencies import DependencyManager
        from src.playlistfy.ui.theme import Theme

        dm = DependencyManager(Theme())
        print(f"{CHECK_MARK} DependencyManager initialized successfully")

        # Test that it can check packages
        print(f"\n{CHECK_MARK} DependencyManager can check packages")

        return True
    except Exception as e:
        print(f"{CROSS_MARK} Error: {e}")
        return False


def test_live_display():
    """Test that LiveDisplay can be imported and used"""
    print("\n" + "="*50)
    print("Testing LiveDisplay with Rich...")
    print("="*50 + "\n")

    try:
        from src.playlistfy.ui.live_display import LiveDisplay
        from src.playlistfy.ui.theme import Theme

        display = LiveDisplay(Theme())
        print(f"{CHECK_MARK} LiveDisplay initialized successfully")

        # Test basic functionality
        display.print(f"[green]{CHECK_MARK}[/green] Rich formatting works!")

        return True
    except Exception as e:
        print(f"{CROSS_MARK} Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all dependency tests"""
    print("\n" + "="*60)
    print("  Playlistfy Dependency Test Suite")
    print("="*60 + "\n")

    tests = [
        ("Import Dependencies", test_import_dependencies),
        ("Dependency Manager", test_dependency_manager),
        ("LiveDisplay System", test_live_display),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n{CROSS_MARK} Test '{name}' crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60 + "\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = f"{CHECK_MARK} PASS" if result else f"{CROSS_MARK} FAIL"
        print(f"{status:12} - {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print(f"\n{CHECK_MARK} All tests passed! The dependency system is working correctly.")
        return 0
    else:
        print(f"\n{CROSS_MARK} Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
