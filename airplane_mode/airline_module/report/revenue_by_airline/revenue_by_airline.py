import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum

def execute(filters=None):
    columns = [
        {"fieldname": "airline", "label": "Airline", "fieldtype": "Link", "options": "Airline", "width": 200},
        {"fieldname": "revenue", "label": "Revenue", "fieldtype": "Currency", "width": 150}
    ]

    airline_master = DocType("Airline")
    ticket_doc = DocType("Airplane Ticket")
    flight_doc = DocType("Airplane Flight")
    airplane_doc = DocType("Airplane")

    # 1. Fetch all airlines in the system to ensure 0-revenue ones are included
    all_airlines = frappe.qb.from_(airline_master).select(airline_master.name).run(pluck=True)

    # 2. Query revenue grouped by airline via multi-table join
    revenue_data = (
        frappe.qb.from_(ticket_doc)
        .join(flight_doc)
        .on(ticket_doc.flight == flight_doc.name)
        .join(airplane_doc)
        .on(flight_doc.airplane == airplane_doc.name)
        .select(
            airplane_doc.airline.as_("airline"),
            Sum(ticket_doc.total_amount).as_("revenue")
        )
        .where(ticket_doc.docstatus == 1)
        .groupby(airplane_doc.airline)
        .run(as_dict=True)
    )

    revenue_map = {row.airline: row.revenue or 0 for row in revenue_data}

    data = []
    total_revenue = 0

    # 3. Build dataset ensuring all airlines appear
    for airline in all_airlines:
        rev = revenue_map.get(airline, 0)
        total_revenue += rev
        data.append({
            "airline": airline,
            "revenue": rev
        })

    # Sort data by revenue descending
    data = sorted(data, key=lambda x: x["revenue"], reverse=True)

    # 4. Add total row at the bottom
    data.append({
        "airline": "Total",
        "revenue": total_revenue
    })

    # 5. Summary Section for Total Revenue card
    report_summary = [
        {
            "value": total_revenue,
            "indicator": "Green",
            "label": "Total Revenue",
            "datatype": "Currency"
        }
    ]

    # 6. Donut Chart Configuration
    chart = {
        "type": "donut",
        "data": {
            "labels": [row["airline"] for row in data if row["airline"] != "Total" and row["revenue"] > 0],
            "datasets": [
                {
                    "values": [row["revenue"] for row in data if row["airline"] != "Total" and row["revenue"] > 0]
                }
            ]
        }
    }

    return columns, data, None, chart, report_summary


def execute_snapshot_report(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for snapshot report. When 'Synced
	Report' is enabled in report, framework will call this method
	every time the report is refreshed or a filter is updated. It
	accepts the same filters as normal execute. But a utility method -
	get_latest_sync, is also imported.

	"""
	from frappe.database.duckdb.database import get_latest_sync

	columns, data = [], []
	return columns, data
