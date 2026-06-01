from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from curso.db import get_connection

NOTA_MINIMA_APROBACION = 4


def _build_pdf_response(title, headers, rows, landscape_mode=False):
    buffer = BytesIO()
    page_size = landscape(A4) if landscape_mode else A4
    doc = SimpleDocTemplate(buffer, pagesize=page_size, topMargin=2*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph(title, styles["Title"]))
    elements.append(Spacer(1, 0.5 * cm))

    table_data = [headers] + rows
    col_count = len(headers)
    col_width = (page_size[0] - 4 * cm) / col_count

    table = Table(table_data, colWidths=[col_width] * col_count, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ]))

    elements.append(table)
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def _build_estadisticas_pdf(summary_headers, summary_rows, detail_headers, detail_rows):
    buffer = BytesIO()
    page_size = A4
    doc = SimpleDocTemplate(buffer, pagesize=page_size, topMargin=2*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Estadísticas de Aprobación", styles["Title"]))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph("Resumen General", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * cm))

    summary_table = Table(
        [summary_headers] + summary_rows,
        colWidths=[8 * cm, 6 * cm],
        repeatRows=1,
    )
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph("Detalle por Evaluación", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * cm))

    col_count = len(detail_headers)
    col_width = (page_size[0] - 4 * cm) / col_count
    detail_table = Table(
        [detail_headers] + detail_rows,
        colWidths=[col_width] * col_count,
        repeatRows=1,
    )
    detail_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ]))
    elements.append(detail_table)
    doc.build(elements)

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def informe_alumnos(curso_id, abandono=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if abandono is not None:
        query = """
            SELECT legajo, nombre, apellido, email, abandono
            FROM alumnos
            WHERE curso_id = %s AND abandono = %s
            ORDER BY apellido, nombre
        """
        cursor.execute(query, (curso_id, abandono))
    else:
        query = """
            SELECT legajo, nombre, apellido, email, abandono
            FROM alumnos
            WHERE curso_id = %s
            ORDER BY apellido, nombre
        """
        cursor.execute(query, (curso_id,))

    alumnos = cursor.fetchall()
    cursor.close()
    connection.close()

    headers = ["Legajo", "Nombre", "Apellido", "Email", "Abandono"]
    rows = [
        [
            str(a["legajo"]),
            a["nombre"],
            a["apellido"],
            a["email"],
            "Sí" if a["abandono"] else "No",
        ]
        for a in alumnos
    ]

    return _build_pdf_response("Informe de Alumnos", headers, rows)


def informe_estadisticas(curso_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS total FROM alumnos WHERE curso_id = %s", (curso_id,))
        total_alumnos = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM alumnos WHERE abandono = TRUE AND curso_id = %s", (curso_id,))
        total_abandonos = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS total FROM alumnos WHERE abandono = FALSE AND curso_id = %s", (curso_id,)
        )
        total_activos = cursor.fetchone()["total"]

        cursor.execute("SELECT id, nombre FROM tipos_evaluacion ORDER BY id")
        evaluaciones = cursor.fetchall()

        stats_rows = []
        for ev in evaluaciones:
            cursor.execute(
                """
                SELECT
                    COUNT(*) AS total_notas,
                    AVG(n.nota) AS promedio,
                    SUM(CASE WHEN n.nota >= %s THEN 1 ELSE 0 END) AS aprobados,
                    SUM(CASE WHEN n.nota < %s THEN 1 ELSE 0 END) AS desaprobados
                FROM notas n
                INNER JOIN alumnos a ON n.id_alumno = a.id
                WHERE n.id_evaluacion = %s AND a.abandono = FALSE AND a.curso_id = %s
                """,
                (NOTA_MINIMA_APROBACION, NOTA_MINIMA_APROBACION, ev["id"], curso_id),
            )
            row = cursor.fetchone()
            total_notas = row["total_notas"] or 0
            promedio = (
                f'{float(row["promedio"]):.2f}'
                if total_notas > 0 and row["promedio"] is not None
                else "N/A"
            )
            stats_rows.append([
                ev["nombre"],
                total_notas,
                promedio,
                row["aprobados"] or 0,
                row["desaprobados"] or 0,
            ])
    finally:
        cursor.close()
        connection.close()

    headers = ["Evaluación", "Notas Cargadas", "Promedio", "Aprobados", "Desaprobados"]
    summary_rows = [
        ["Total Alumnos", str(total_alumnos)],
        ["Alumnos Activos", str(total_activos)],
        ["Abandonos", str(total_abandonos)],
        ["Tasa de Abandono", f"{(total_abandonos / total_alumnos * 100) if total_alumnos else 0:.1f}%"],
        [f"Nota mínima de aprobación", str(NOTA_MINIMA_APROBACION)],
    ]

    return _build_estadisticas_pdf(
        ["Métrica", "Valor"], summary_rows,
        headers, stats_rows,
    )


def informe_equipos(curso_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            g.id AS id_grupo,
            g.nombre_grupo,
            g.curso_id,
            a.id AS id_alumno,
            a.legajo,
            a.nombre,
            a.apellido,
            a.email
        FROM grupos g
        LEFT JOIN grupo_integrantes gi ON g.id = gi.id_grupo
        LEFT JOIN alumnos a ON gi.id_alumno = a.id
        WHERE g.curso_id = %s
        ORDER BY g.curso_id, g.nombre_grupo, a.apellido, a.nombre
    """
    cursor.execute(query, (curso_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    grupos_dict = {}
    for row in results:
        grupo_id = row["id_grupo"]
        if grupo_id not in grupos_dict:
            grupos_dict[grupo_id] = {
                "nombre":      row["nombre_grupo"],
                "curso_id":    row["curso_id"],
                "integrantes": [],
            }
        if row["id_alumno"]:
            grupos_dict[grupo_id]["integrantes"].append(
                f'{row["legajo"]} - {row["apellido"]}, {row["nombre"]}'
            )

    headers = ["Grupo", "Curso ID", "Integrantes"]
    rows = [
        [
            data["nombre"],
            str(data["curso_id"]),
            "\n".join(data["integrantes"]) if data["integrantes"] else "Sin integrantes"
        ]
        for data in grupos_dict.values()
    ]

    return _build_pdf_response("Informe de Grupos", headers, rows, landscape_mode=True)
