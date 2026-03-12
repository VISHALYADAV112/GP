# reports-service - Report Generation

Generate PDF and Excel reports for all namunas.

## 📦 Responsibilities

- Generate namuna-specific PDFs
- Export to Excel
- Dashboard analytics
- Audit trail reports

## 📁 Structure

```
reports-service/
├── generators/
│   ├── pdf_generator.py      # ReportLab
│   ├── excel_generator.py    # openpyxl
│   └── templates/             # Report templates
├── reports/
│   ├── financial_reports.py
│   ├── revenue_reports.py
│   └── asset_reports.py
└── README.md
```

## 🎯 Features

- All 33 namuna PDF templates
- Excel exports with formatting
- Custom date range reports
- Aggregated analytics

## 📦 Dependencies

```
reportlab>=4.0.0
openpyxl>=3.1.0
pandas>=2.0.0
```
