# Run on an agent

The hello world run, sent to a machine running `cairnml-agent` instead of running on this one. The script is the same, with one added line: `task.execute_remotely(queue_name="default")`. The agent runs the script, and the run is recorded on your server exactly as before.

## Features

- Queues the run on the `default` queue and stops the local process.
- The agent takes the run from the queue, runs it in a container and records it on your server.
- The run goes from **Queued** to **Running** to **Completed** in the web app.

## Prerequisites

- The [SDK connected to your server](../../README.md#prerequisites)
- An agent on a machine with Docker, taking jobs from the `default` queue. Step 3 of the [walk-through](../../README.md#walk-through-from-a-local-run-to-an-agent) starts one.
- The repository on GitHub, with your changes committed and pushed. The agent clones the repository and runs the script from the commit the run recorded. For a private repository, the agent's git credentials are set in its configuration file by hand (see the [agent README](https://github.com/gianlucapargaetzi/cairnml-agent#connect-to-your-server)).

## Run

Start the agent first (walk-through, step 3), then from this folder:

```bash
python run_on_agent.py
```

The local process logs two warnings and exits:

```
Switching to remote execution, output log page http://<server-ip>/cairnml/...
CairnML Terminating local execution process - continuing execution remotely
```

The command returns straight away. The agent does the rest.

## What to look for

Open the web app and go to the project **examples**, task **run on an agent**:

- The status goes from **Queued** to **Running** to **Completed**. The **Workers & Queues** page shows the job on the queue while it waits, and the agent's machine while it runs.
- The `loss` curve, one point per step, is under scalars.
- `hello.txt` is listed under artifacts.
- The **Console** tab shows the output of the script as it ran on the agent, including the `done:` line.

If the task stays **Queued**, no agent is listening on the `default` queue. Check the agent with `cairnml-agent daemon --queue default --docker` running on that machine.

## Next steps

Back to the [walk-through](../../README.md#walk-through-from-a-local-run-to-an-agent) to see the whole path, or to the [examples](../..) list.
