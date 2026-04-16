def extract_savings(rec):
    try:
        if rec.primary_impact and rec.primary_impact.cost_projection:
            return float(rec.primary_impact.cost_projection.cost.units or 0)
    except:
        pass
    return 0


def extract_category(rec):
    try:
        return rec.primary_impact.category.name
    except:
        return "UNKNOWN"


def extract_priority(rec):
    try:
        return rec.priority.name
    except:
        return "UNKNOWN"


def extract_resource(rec):
    try:
        return rec.name.split("/")[-1]
    except:
        return "N/A"