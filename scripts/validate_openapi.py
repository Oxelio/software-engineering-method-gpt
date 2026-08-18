#!/usr/bin/env python3
from pathlib import Path
import sys, yaml

path = Path(__file__).resolve().parents[1] / "openapi" / "github-repository-orchestrator.openapi.yaml"
spec = yaml.safe_load(path.read_text(encoding="utf-8"))
errors=[]
if spec.get("openapi") != "3.1.0": errors.append("openapi must be 3.1.0")
for key in ("info","servers","paths","components"):
    if key not in spec: errors.append(f"missing top-level key: {key}")

ids=[]
for p, item in spec.get("paths",{}).items():
    for method, op in item.items():
        if method.lower() not in {"get","post","put","patch","delete","options","head","trace"}: continue
        oid=op.get("operationId")
        if not oid: errors.append(f"missing operationId: {method.upper()} {p}")
        else: ids.append(oid)
if len(ids) != len(set(ids)):
    errors.append("operationId values are not unique")

def resolve_ref(ref):
    if not ref.startswith("#/"): return True
    cur=spec
    try:
        for part in ref[2:].split('/'):
            cur=cur[part.replace('~1','/').replace('~0','~')]
        return True
    except Exception:
        return False

def walk(v):
    if isinstance(v,dict):
        if "$ref" in v and not resolve_ref(v["$ref"]): errors.append(f"unresolved ref: {v['$ref']}")
        for x in v.values(): walk(x)
    elif isinstance(v,list):
        for x in v: walk(x)
walk(spec)

gql=spec.get("paths",{}).get("/graphql",{}).get("post",{})
try:
    reqref=gql["requestBody"]["content"]["application/json"]["schema"]["$ref"]
    req=spec["components"]["schemas"][reqref.split('/')[-1]]
    qref=req["properties"]["query"]
    enum=qref.get("enum",[])
    if not enum: errors.append("GraphQL query must remain a non-empty enum allowlist")
    if any(not isinstance(q,str) or not (q.startswith("query(") or q.startswith("mutation(")) for q in enum):
        errors.append("invalid GraphQL allowlist entry")
except Exception as e:
    errors.append(f"cannot validate GraphQL allowlist: {e}")

if errors:
    print("OpenAPI validation FAILED")
    for e in errors: print("-",e)
    sys.exit(1)
print(f"OpenAPI validation OK: {len(ids)} operations, {len(enum)} allowlisted GraphQL operations")
