import pyautogui
import time
from pynput import keyboard

# 全局配置
pyautogui.FAILSAFE = True  # 安全模式：移动到屏幕左上角可中断
running = True
operation_interval = 0.5  # 默认操作间隔时间

# 选择操作间隔时间
def select_interval():
    global operation_interval
    print("请选择操作间隔时间：")
    print("1. 0.2秒")
    print("2. 0.5秒")
    
    while True:
        choice = input("请输入选项 (1 或 2): ").strip()
        if choice == '1':
            operation_interval = 0.2
            print("已选择操作间隔时间: 0.2秒")
            break
        elif choice == '2':
            operation_interval = 0.5
            print("已选择操作间隔时间: 0.5秒")
            break
        else:
            print("无效的选项，请重新输入1或2。")

# 坐标配置
coordinates = [(409, 372), (648, 377), (896, 369), (1132, 373), 
               (409, 751), (653, 755), (889, 753), (1134, 758)]

# 循环结束后换页操作
end_cycle_click = {"x": 1253, "y": 543, "button": "left", "clicks": 1}

# 操作序列模板（第一个操作的坐标会被替换）
base_operations = [
    {"x": None, "y": None, "button": "right", "clicks": 1},
    {"x": 801, "y": 914, "button": "left", "clicks": 1},
    {"x": 827, "y": 654, "button": "left", "clicks": 2},
    {"x": 1737, "y": 478, "button": "left", "clicks": 1}
]

# 键盘事件监听函数
def on_press(key):
    global running
    try:
        if key.char == 'e':
            print("\n检测到'e'键按下，程序将终止...")
            running = False
            return False  # 停止监听
    except AttributeError:
        pass

# 主程序开始
select_interval()

print(f"\n5秒后开始执行自动化点击操作...")
print("注意：操作期间请不要移动鼠标，如需中断，请快速将鼠标移动到屏幕左上角或按下'e'键")

# 启动键盘监听
listener = keyboard.Listener(on_press=on_press)
listener.start()

# 准备时间
time.sleep(5)

cycle_count = 0

# 主循环执行
while running:
    cycle_count += 1
    print(f"\n========== 开始Kill第 {cycle_count} 页 ==========")
    
    for coord_index, (x, y) in enumerate(coordinates, 1):
        if not running:
            break
            
        print(f"\n开始处理 {coord_index}/{len(coordinates)}: ({x}, {y})")
        
        # 设置当前坐标的操作序列
        current_operations = [op.copy() for op in base_operations]
        current_operations[0]["x"] = x
        current_operations[0]["y"] = y
        
        for op_index, op in enumerate(current_operations, 1):
            if not running:
                break
                
            
            # 执行鼠标操作
            pyautogui.moveTo(op['x'], op['y'])
            time.sleep(0.2)
            
            if op['clicks'] == 1:
                pyautogui.click(button=op['button'])
            else:
                pyautogui.click(button=op['button'], clicks=op['clicks'], interval=0.1)
            
            if op_index < len(current_operations):
                time.sleep(operation_interval)
        
        # 坐标组间隔
        if coord_index < len(coordinates) and running:
            time.sleep(operation_interval)
    
    if not running:
        break
        
    # 循环结束后换页
    pyautogui.moveTo(end_cycle_click["x"], end_cycle_click["y"])
    time.sleep(0.2)
    pyautogui.click(button=end_cycle_click["button"])
    time.sleep(operation_interval)

# 程序结束
listener.join()
print("\n程序已成功终止！")
print(f"总共Kill了 {cycle_count} 页。")
