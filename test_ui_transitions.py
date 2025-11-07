"""
Test script to demonstrate smooth UI transitions
"""
import time
from src.playlistfy.ui.theme import Theme
from src.playlistfy.ui.live_display import LiveDisplay

def test_spinner_to_progress():
    """Test spinner → progress bar transition"""
    print("\n=== Test 1: Spinner to Progress Bar Transition ===\n")

    theme = Theme()
    display = LiveDisplay(theme)

    def download_task(progress):
        task = progress.add_task("Downloading video.mp4", total=100)
        for i in range(100):
            time.sleep(0.05)
            progress.update(task, advance=1)

    display.transition_spinner_to_progress(
        "Preparing download...",
        download_task
    )

    display.print_status("Download complete!", status="success")


def test_smooth_spinner():
    """Test smooth spinner context"""
    print("\n=== Test 2: Smooth Spinner ===\n")

    theme = Theme()
    display = LiveDisplay(theme)

    with display.spinner_context("Fetching playlist information..."):
        time.sleep(2)

    display.print_status("Playlist fetched successfully", status="success")


def test_scroll_in():
    """Test scroll-in content reveal"""
    print("\n=== Test 3: Scroll-In Content Reveal ===\n")

    theme = Theme()
    display = LiveDisplay(theme)

    display.print_section_header("Playlist Videos")

    lines = [
        "[cyan bold]  1.[/cyan bold] Introduction to Python",
        "     [dim]Duration: 15:30[/dim]",
        "",
        "[cyan bold]  2.[/cyan bold] Variables and Data Types",
        "     [dim]Duration: 22:45[/dim]",
        "",
        "[cyan bold]  3.[/cyan bold] Control Flow and Loops",
        "     [dim]Duration: 18:20[/dim]",
        "",
        "[cyan bold]  4.[/cyan bold] Functions and Modules",
        "     [dim]Duration: 25:10[/dim]",
        "",
        "[cyan bold]  5.[/cyan bold] Object-Oriented Programming",
        "     [dim]Duration: 32:00[/dim]",
    ]

    display.scroll_in_content(lines, delay=0.05)


def test_progress_context():
    """Test progress context with multiple tasks"""
    print("\n=== Test 4: Multiple Progress Tasks ===\n")

    theme = Theme()
    display = LiveDisplay(theme)

    with display.progress_context("Downloading playlist") as progress:
        # Simulate downloading 3 videos
        tasks = [
            progress.add_task("Video 1.mp4", total=100),
            progress.add_task("Video 2.mp4", total=100),
            progress.add_task("Video 3.mp4", total=100),
        ]

        for i in range(100):
            time.sleep(0.03)
            for task in tasks:
                progress.update(task, advance=1)

    display.print_status("All videos downloaded", status="success")


def test_status_messages():
    """Test different status message styles"""
    print("\n=== Test 5: Status Message Styles ===\n")

    theme = Theme()
    display = LiveDisplay(theme)

    display.print_status("Operation started successfully", status="success")
    time.sleep(0.5)

    display.print_status("Processing data...", status="info")
    time.sleep(0.5)

    display.print_status("Warning: Rate limit approaching", status="warning")
    time.sleep(0.5)

    display.print_status("Error: Connection timeout", status="error")


def test_completion_summary():
    """Test completion summary table"""
    print("\n=== Test 6: Completion Summary ===\n")

    theme = Theme()
    display = LiveDisplay(theme)

    items = [
        {"name": "Video 1: Introduction", "status": "success", "details": "25.3 MB"},
        {"name": "Video 2: Tutorial", "status": "success", "details": "42.1 MB"},
        {"name": "Video 3: Advanced", "status": "error", "details": "Network timeout"},
        {"name": "Video 4: Summary", "status": "success", "details": "18.7 MB"},
    ]

    display.show_completion_summary("Download Results", items)


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Playlistfy UI Transitions Test Suite")
    print("="*60)

    try:
        test_smooth_spinner()
        time.sleep(1)

        test_spinner_to_progress()
        time.sleep(1)

        test_scroll_in()
        time.sleep(1)

        test_progress_context()
        time.sleep(1)

        test_status_messages()
        time.sleep(1)

        test_completion_summary()

        print("\n" + "="*60)
        print("  All tests completed successfully!")
        print("="*60 + "\n")

    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\nError during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
