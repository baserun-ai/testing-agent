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

## Datadog

Sign up for Datadog, install a Datadog agent locally, and then run with `ddtrace-run`:

```bash
DD_API_KEY=MY_API_KEY DD_OPENAI_LOGS_ENABLED=1 poetry run ddtrace-run python demo/main.py
```

Then look at APM: https://us5.datadoghq.com/apm/traces