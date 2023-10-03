# Baserun demo

This is a small app that uses LangChain to demonstrate Baserun.

## Walkthrough

### Setup

```bash
$ poetry install
```

### Execute the main.py script

```bash
$ python demo/main.py
```

If passed without arguments it will prompt you for a task. You can pass an argument for the task if you wish:

```bash
python demo/main.py "tell me the capital of the united states"
```

### It will prompt you for what you want to do

```
What would you like me to do?
> Tell me the capital of the united states
```

## After this step everything is automatic

After you provide input you can sit back and watch it accomplish its task.

## Command line arguments

```
positional arguments:
  user_input            User input for the agent.

options:
  --provider            {openai,anthropic}
                        Specify the provider.
  --use_streaming       Enable streaming.
  --agent_type          Type of the agent
```