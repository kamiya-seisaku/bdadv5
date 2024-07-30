import bpy
import win32gui

# return first 3d viewport position/size relative to the display
def get_3dview_position():
    # Ensure there's at least one 3D Viewport
    if not any(area.type == 'VIEW_3D' for area in bpy.context.screen.areas):
        raise ValueError("No 3D Viewport found!")

    # Find the first 3D Viewport
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            view_3d_area = area
            break

    # Get region (area inside the viewport that displays 3D content)
    region = view_3d_area.regions[-1] 

    # Get the window coordinates of the viewport
    x1 = view_3d_area.x
    y1 = view_3d_area.y

    # Calculate the coordinates of the bottom right corner
    x2 = x1 + view_3d_area.width
    y2 = y1 + view_3d_area.height

    # Blender window position
    x1w, y1w, x2w, y2w = get_window_position("Blender")

    # return 3d view window position/size relative to the display

    print(f"3d Viewport position: ({x1}, {y1}) - ({x2}, {y2})")
    print(f"area width: {view_3d_area.width}, area height: {view_3d_area.height}")
    print(f"Blender window position: ({x1w}, {y1w}) - ({x2w}, {y2w})")
    return x1 + x1w, y1 + y1w, x2 + x1w, y2 + y1w

def test_get_3dview_position():
    x1, y1, x2, y2 = get_3dview_position()
    print(f"3D Viewport Position: ({x1}, {y1}) - ({x2}, {y2})")

#obtain windows window position, to obtain blender window position
def get_window_position(target_title):
    def enum_callback(hwnd, lparam):
        title = win32gui.GetWindowText(hwnd)
        if target_title in title:
            rect = win32gui.GetWindowRect(hwnd)
            lparam.append(rect)  # Store the coordinates in the list

    windows = []
    win32gui.EnumWindows(enum_callback, windows)

    if windows:
        return windows[0]  # Return the first matching window
    else:
        return None  # Return None if no window is found

def test_get_window_position():
    # Get the window title you want to find (case-sensitive!)
    target_title = "Blender"  # Replace with your desired window title

    window_position = get_window_position(target_title)

    if window_position:
        x1, y1, x2, y2 = window_position
        print(f"Window '{target_title}' Position: ({x1}, {y1}) - ({x2}, {y2})")
    else:
        print(f"Window '{target_title}' not found.")

test_get_3dview_position()
