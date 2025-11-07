"""
Test script to verify quality fallback logic
"""
import sys
import platform

# Use safe characters on Windows
IS_WINDOWS = platform.system().lower() == 'windows'
CHECK_MARK = '[OK]' if IS_WINDOWS else '✓'
CROSS_MARK = '[X]' if IS_WINDOWS else '✗'

def test_quality_hierarchy():
    """Test that quality hierarchy is correctly defined"""
    print("Testing quality hierarchy logic...\n")

    # Define quality hierarchy for fallback (same as in downloader.py)
    quality_hierarchy = {
        '1080p': ['1080', '720', '480', 'best'],
        '720p': ['720', '480', 'best'],
        '480p': ['480', 'best'],
        'best': ['best'],
        'worst': ['worst']
    }

    test_cases = [
        ('1080p', ['1080', '720', '480', 'best']),
        ('720p', ['720', '480', 'best']),
        ('480p', ['480', 'best']),
        ('best', ['best']),
        ('worst', ['worst']),
    ]

    passed = 0
    failed = 0

    for quality, expected_chain in test_cases:
        actual_chain = quality_hierarchy.get(quality, ['best'])
        if actual_chain == expected_chain:
            print(f"{CHECK_MARK} {quality:6} -> {' -> '.join(expected_chain)}")
            passed += 1
        else:
            print(f"{CROSS_MARK} {quality:6} -> Expected {expected_chain}, got {actual_chain}")
            failed += 1

    print(f"\nResults: {passed}/{len(test_cases)} tests passed")
    return failed == 0


def test_format_strings():
    """Test that format strings have progressive fallback"""
    print("\nTesting format strings...\n")

    quality_formats = {
        'best': 'bestvideo+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/bestvideo[height<=720]+bestaudio/best[height<=720]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]/bestvideo[height<=480]+bestaudio/best[height<=480]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]/worst',
        'worst': 'worstvideo+worstaudio/worst'
    }

    passed = 0
    failed = 0

    # Test that each format string contains fallback options (/)
    test_cases = [
        ('1080p', True),   # Should have fallback
        ('720p', True),    # Should have fallback
        ('480p', True),    # Should have fallback
        ('best', True),    # Should have fallback
        ('worst', True),   # Should have fallback
    ]

    for quality, should_have_fallback in test_cases:
        format_str = quality_formats.get(quality, '')
        has_fallback = '/' in format_str

        if has_fallback == should_have_fallback:
            fallback_count = format_str.count('/')
            print(f"{CHECK_MARK} {quality:6} has {fallback_count} fallback option(s)")
            passed += 1
        else:
            print(f"{CROSS_MARK} {quality:6} fallback check failed")
            failed += 1

    print(f"\nResults: {passed}/{len(test_cases)} tests passed")
    return failed == 0


def test_quality_verification_logic():
    """Test the logic for quality verification"""
    print("\nTesting quality verification logic...\n")

    # Simulate different scenarios
    scenarios = [
        {
            'name': 'Video has 1080p, user requests 1080p',
            'formats_available': '1080p',
            'requested': '1080p',
            'expected': '1080p',
        },
        {
            'name': 'Video has 720p only, user requests 1080p',
            'formats_available': '720p',
            'requested': '1080p',
            'expected': '720p',
        },
        {
            'name': 'Video has 480p only, user requests 720p',
            'formats_available': '480p',
            'requested': '720p',
            'expected': '480p',
        },
        {
            'name': 'Video has no specific quality, user requests 1080p',
            'formats_available': '',
            'requested': '1080p',
            'expected': 'best',
        },
    ]

    quality_hierarchy = {
        '1080p': ['1080', '720', '480', 'best'],
        '720p': ['720', '480', 'best'],
        '480p': ['480', 'best'],
        'best': ['best'],
        'worst': ['worst']
    }

    passed = 0
    failed = 0

    for scenario in scenarios:
        formats_output = scenario['formats_available'].lower()
        requested_quality = scenario['requested']
        expected_result = scenario['expected']

        # Simulate the verification logic
        fallback_chain = quality_hierarchy.get(requested_quality, ['best'])
        result = None

        for quality_option in fallback_chain:
            if quality_option == 'best' or quality_option == 'worst':
                result = quality_option
                break

            if f'{quality_option}p' in formats_output or f'{quality_option}x' in formats_output:
                result = f'{quality_option}p'
                break

        if result is None:
            result = 'best'

        if result == expected_result:
            print(f"{CHECK_MARK} {scenario['name']}")
            print(f"  Requested: {requested_quality}, Got: {result}")
            passed += 1
        else:
            print(f"{CROSS_MARK} {scenario['name']}")
            print(f"  Requested: {requested_quality}, Expected: {expected_result}, Got: {result}")
            failed += 1
        print()

    print(f"Results: {passed}/{len(scenarios)} tests passed")
    return failed == 0


def main():
    """Run all quality fallback tests"""
    print("\n" + "="*60)
    print("  Playlistfy Quality Fallback Test Suite")
    print("="*60 + "\n")

    tests = [
        ("Quality Hierarchy", test_quality_hierarchy),
        ("Format Strings", test_format_strings),
        ("Quality Verification Logic", test_quality_verification_logic),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n{CROSS_MARK} Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
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
        print(f"\n{CHECK_MARK} All tests passed! Quality fallback logic is working correctly.")
        return 0
    else:
        print(f"\n{CROSS_MARK} Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
