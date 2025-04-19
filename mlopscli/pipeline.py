# mlopscli/pipeline.py
import subprocess


def topological_sort(steps: dict):
    from collections import defaultdict, deque

    graph = defaultdict(list)
    indegree = defaultdict(int)

    for name, step in steps.items():
        for dep in step.get("depends_on", []):
            graph[dep].append(name)
            indegree[name] += 1

    queue = deque([name for name in steps if indegree[name] == 0])
    sorted_steps = []

    while queue:
        node = queue.popleft()
        sorted_steps.append(steps[node])
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_steps) != len(steps):
        raise ValueError("Cycle detected in job dependencies!")

    return sorted_steps


def execute_scripts(steps_dict):
    sorted_steps = topological_sort(steps_dict)

    for step in sorted_steps:
        name = step["name"]
        script = step["script"]
        print(f"\n🔧 Running step: {name} ({script})")

        result = subprocess.run(["python", str(script)], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Step '{name}' failed.")
            print(result.stderr)
            break
        else:
            print(f"✅ Step '{name}' completed.")
            print(result.stdout)
