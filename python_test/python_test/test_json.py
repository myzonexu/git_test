import json
from dataclasses import dataclass

@dataclass
class TaskState:
    #['任务ID', 'robot_ID', '起点', '终点','途经点', '优先级', '等待信号']
    id : int
    robot_id : int=0
    start_point : int=0
    end_point : int=0
    way_point :int=0
    priority : int=0
    wait_button : int =0


table_task_state=[]

for id in range(10):
    table_task_state.append(TaskState(id))

print(table_task_state[0].__dict__)
json_str = json.dumps(table_task_state, default=lambda o: o.__dict__, indent=4)
print(json_str)

with open('data.json', 'w') as f:
    json.dump(table_task_state,f, default=lambda o: o.__dict__,  indent=4)



