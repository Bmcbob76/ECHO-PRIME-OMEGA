    async def _execute_window_control(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute window control tools using Win32 APIs - no cursor movement"""
        if not WIN32_AVAILABLE:
            return {
                "success": False,
                "error": "pywin32 not available. Install with: pip install pywin32"
            }
        
        try:
            if name == "window_list":
                windows = []
                def callback(hwnd, extra):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if title:
                            windows.append({
                                "handle": hwnd,
                                "title": title,
                                "class": win32gui.GetClassName(hwnd)
                            })
                
                win32gui.EnumWindows(callback, None)
                return {
                    "success": True,
                    "windows": windows,
                    "count": len(windows)
                }
            
            elif name == "window_find":
                title_search = arguments.get("title", "").lower()
                found_windows = []
                
                def callback(hwnd, extra):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if title and title_search in title.lower():
                            found_windows.append({
                                "handle": hwnd,
                                "title": title,
                                "class": win32gui.GetClassName(hwnd)
                            })
                
                win32gui.EnumWindows(callback, None)
                return {
                    "success": True,
                    "windows": found_windows,
                    "count": len(found_windows)
                }
            
            elif name == "window_click":
                title_search = arguments.get("window_title", "").lower()
                x = int(arguments.get("x"))
                y = int(arguments.get("y"))
                button = arguments.get("button", "left")
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Calculate lparam for position
                lparam = win32api.MAKELONG(x, y)
                
                # Send click messages (down + up)
                if button == "left":
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
                    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)
                elif button == "right":
                    win32api.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lparam)
                    win32api.SendMessage(hwnd, win32con.WM_RBUTTONUP, 0, lparam)
                
                return {
                    "success": True,
                    "action": "window_click",
                    "window": win32gui.GetWindowText(hwnd),
                    "position": {"x": x, "y": y},
                    "button": button
                }
            
            elif name == "window_type":
                title_search = arguments.get("window_title", "").lower()
                text = arguments.get("text", "")
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Send WM_CHAR for each character
                for char in text:
                    win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(char), 0)
                
                return {
                    "success": True,
                    "action": "window_type",
                    "window": win32gui.GetWindowText(hwnd),
                    "text": text,
                    "length": len(text)
                }
            
            elif name == "window_send_keys":
                title_search = arguments.get("window_title", "").lower()
                keys = arguments.get("keys", [])
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Map key names to virtual key codes
                vk_map = {
                    "enter": win32con.VK_RETURN,
                    "tab": win32con.VK_TAB,
                    "esc": win32con.VK_ESCAPE,
                    "space": win32con.VK_SPACE,
                    "ctrl": win32con.VK_CONTROL,
                    "alt": win32con.VK_MENU,
                    "shift": win32con.VK_SHIFT,
                    "delete": win32con.VK_DELETE,
                    "backspace": win32con.VK_BACK,
                    "home": win32con.VK_HOME,
                    "end": win32con.VK_END,
                    "pageup": win32con.VK_PRIOR,
                    "pagedown": win32con.VK_NEXT,
                }
                
                # Send key down for all keys
                for key in keys:
                    vk = vk_map.get(key.lower(), ord(key.upper()))
                    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, vk, 0)
                
                # Send key up in reverse order
                for key in reversed(keys):
                    vk = vk_map.get(key.lower(), ord(key.upper()))
                    win32api.SendMessage(hwnd, win32con.WM_KEYUP, vk, 0)
                
                return {
                    "success": True,
                    "action": "window_send_keys",
                    "window": win32gui.GetWindowText(hwnd),
                    "keys": keys
                }
            
            elif name == "window_focus":
                title_search = arguments.get("window_title", "").lower()
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Bring to foreground
                win32gui.SetForegroundWindow(hwnd)
                
                return {
                    "success": True,
                    "action": "window_focus",
                    "window": win32gui.GetWindowText(hwnd)
                }
            
            elif name == "window_get_rect":
                title_search = arguments.get("window_title", "").lower()
                
                # Find window
                hwnd = None
                def callback(h, extra):
                    nonlocal hwnd
                    if win32gui.IsWindowVisible(h):
                        title = win32gui.GetWindowText(h)
                        if title and title_search in title.lower():
                            hwnd = h
                            return False
                
                win32gui.EnumWindows(callback, None)
                
                if not hwnd:
                    return {"success": False, "error": f"Window not found: {title_search}"}
                
                # Get window rectangle
                rect = win32gui.GetWindowRect(hwnd)
                
                return {
                    "success": True,
                    "window": win32gui.GetWindowText(hwnd),
                    "rect": {
                        "left": rect[0],
                        "top": rect[1],
                        "right": rect[2],
                        "bottom": rect[3],
                        "width": rect[2] - rect[0],
                        "height": rect[3] - rect[1]
                    }
                }
            
            return {"success": False, "error": f"Unknown window control tool: {name}"}
            
        except Exception as e:
            logger.error(f"Window control error: {name} - {str(e)}")
            return {
                "success": False,
                "error": f"Window control failed: {str(e)}"
            }
