# EchoChain Dashboard

## Requirements

- Power BI Desktop
- MySQL Server
- EchoChain Database

## Setup

1. Pull latest code

```bash
git pull origin main
```

2. Run

```bash
python scripts/merge_data.py
python scripts/kpi_generation.py
```

3. Open

```
dashboard/EchoChain.pbix
```

4. Click Refresh

## Collaboration Workflow

1. Always pull before editing

```bash
git pull
```

2. Save the dashboard

3. Commit

```bash
git add dashboard/EchoChain.pbix
git commit -m "Updated dashboard"
git push
```

4. Inform teammates before editing the `.pbix` file to avoid conflicts.