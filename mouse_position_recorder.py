import pyautogui
import keyboard
import time
from pynput import mouse

# 全局变量
recorded_positions = []  # 存储记录的坐标
running = True


def on_click(x, y, button, pressed):
    if not running:
        return False
        
    if button == mouse.Button.left and pressed:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        
        position_info = {
            'timestamp': current_time,
            'x': int(x),
            'y': int(y)
        }
        recorded_positions.append(position_info)
        
        print(f"[{current_time}] 记录位置: X={int(x)}, Y={int(y)}")
        print(f"当前已记录 {len(recorded_positions)} 个位置")
        print("-" * 40)


def exit_program():
    global running
    running = False
    print("\n=== 程序即将退出 ===")
    
    if recorded_positions:
        print(f"\n总共记录了 {len(recorded_positions)} 个鼠标位置：")
        
        for i, pos in enumerate(recorded_positions, 1):
            print(f"{i}. [{pos['timestamp']}] X={pos['x']}, Y={pos['y']}")
        
        coords_list = [(pos['x'], pos['y']) for pos in recorded_positions]
        print("\nPython列表格式的坐标数据（可直接复制使用）：")
        print(coords_list)
    else:
        print("未记录任何鼠标位置")
    
    print("\n程序已退出")
    return False


def show_current_position():
    if not running:
        return
        
    x, y = pyautogui.position()
    print(f"当前鼠标位置: X={x}, Y={y}")


def main():
    print("=== 鼠标点击位置记录工具 ===")
    print("功能说明:")
    print("1. 点击鼠标左键记录当前位置坐标")
    print("2. 按P键显示当前鼠标位置")
    print("3. 按ESC键退出程序")
    print("\n开始记录...")
    
    keyboard.add_hotkey('esc', exit_program)
    keyboard.add_hotkey('p', show_current_position)
    
    with mouse.Listener(on_click=on_click) as listener:
        print("鼠标监听器已启动，移动鼠标并点击左键开始记录坐标...")
        listener.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit_program()
    except Exception as e:
        print(f"程序发生错误: {e}")
        time.sleep(2)