# Cloud Cost Optimizer

**Cloud Cost Optimizer** is a tool to automatically identify idle resources in AWS and Azure cloud environments, generate optimization reports, and send email notifications. It is built with **FastAPI** for reporting and uses **Bash scripts** to interact with cloud services.

---

## Features

* Detect idle AWS EC2 instances and optionally stop them.
* Detect idle Azure Virtual Machines and optionally deallocate them.
* Generate detailed daily cost optimization reports.
* Send automated email notifications with the report.
* FastAPI endpoints to list and retrieve reports.
* Supports dry-run mode to simulate actions before actually stopping resources.

---

## Project Structure

```
cloud-cost-optimizer/
│
├─ main.py                # FastAPI backend to list & view reports, trigger optimization
├─ index.html             # Frontend (optional) to trigger report generation
├─ scripts/
│  ├─ optimize.sh         # Master script to run AWS & Azure optimization and send email
│  ├─ optimize_aws.sh     # AWS optimization script
│  ├─ optimize_azure.sh   # Azure optimization script
│  └─ notify_email.sh     # Script to send reports via email
└─ README.md
```

---

## Requirements

* Python 3.8+
* FastAPI
* `uvicorn` (for running the API)
* AWS CLI configured
* Azure CLI configured
* SMTP-enabled email account (for notifications)
* Bash shell

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Saeedullahshaikh/cloud-cost-optimizer.git
cd cloud-cost-optimizer
```

2. Install Python dependencies:

```bash
pip install fastapi uvicorn
```

3. Configure cloud credentials:

* **AWS:** `aws configure`
* **Azure:** `az login`

4. Update `scripts/notify_email.sh` with your SMTP credentials:

```bash
SMTP_USER="your-email@gmail.com"
SMTP_PASS="your-app-password"
TARGET_EMAIL="recipient@example.com"
```

---

## Usage

### Run FastAPI backend

```bash
uvicorn main:app --reload
```

API Endpoints:

* `GET /reports` – List all reports.
* `GET /reports/{name}` – Get content of a specific report.
* `POST /run` – Manually trigger optimization scripts.

---

### Run Optimization Scripts Manually

```bash
bash scripts/optimize.sh
```

This script will:

1. Run `optimize_aws.sh` to check AWS resources.
2. Run `optimize_azure.sh` to check Azure resources.
3. Generate a report in `/tmp/cost_report_YYYY-MM-DD.txt`.
4. Send the report via email using `notify_email.sh`.

---

### Script Details

* **optimize_aws.sh**

  * Finds idle AWS EC2 instances based on CPU metrics.
  * Stops instances if `DRY_RUN=false`.

* **optimize_azure.sh**

  * Finds idle Azure VMs (CPU < 5%).
  * Deallocates VMs if `DRY_RUN=false`.

* **notify_email.sh**

  * Sends an email with the report.
  * Dynamically sets the subject based on which cloud had idle resources.

* **optimize.sh**

  * Master script coordinating AWS, Azure checks, and email notification.

---

## Cron Scheduling

### — Cron Scheduling

Edit cron:

```bash
crontab -e
```

Add this line:

```bash
0 1 * * * /bin/bash /project-path/scripts/optimize.sh >> /var/log/optimize.log 2>&1
```

This runs the optimization script daily at 1 AM.

---

## Rundeck Scheduling (Optional)

### — Rundeck Scheduling

1. Install Rundeck (Ubuntu):

```bash
sudo apt-get install openjdk-11-jre -y
wget https://repo.rundeck.org/latest.rpm
```

2. Create a job in the Rundeck UI:

* **Command:**

```bash
bash /project-path/scripts/optimize.sh
```

* **Schedule:** daily at 1 AM 

---

## Notes

* All reports are saved in `/tmp` with the format `cost_report_YYYY-MM-DD.txt`.
* Dry-run mode is enabled by default to prevent accidental resource shutdowns.
* Ensure CLI tools (AWS/Azure) are authenticated and have the necessary permissions.

---

## License

This project is open-source. You can modify and use it as per your requirements.

---

## Author

[Saeedullah Shaikh](https://github.com/Saeedullahshaikh)
