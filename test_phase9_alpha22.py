from app.phase9.enrichment_alpha2 import classify_kwja_proposal


def p(start, end, surface, family="grammar", role="grammar"):
    return {"start":start,"end":end,"surface":surface,"candidate_family":family,"proposed_role":role}


def main():
    same = classify_kwja_proposal(p(2,6,"てしまう"), [{"start":2,"end":6,"surface":"てしまう","role":"grammar"}])
    assert same["decision_status"] == "corroborates-existing" and not same["resolver_eligible"]
    repair = classify_kwja_proposal(p(2,6,"でしまう"), [{"start":2,"end":3,"role":"grammar"},{"start":3,"end":4,"role":"unresolved"}])
    assert repair["decision_status"] == "eligible-improvement" and repair["resolver_eligible"]
    coined = classify_kwja_proposal(p(1,5,"寝坊った","term","term"), [{"start":1,"end":2,"role":"term"},{"start":2,"end":4,"role":"term"},{"start":4,"end":5,"role":"particle"}])
    assert coined["decision_status"] == "eligible-structural-repair" and coined["resolver_eligible"]
    evidence = classify_kwja_proposal(p(1,4,"という"), [{"start":1,"end":2,"role":"particle"},{"start":2,"end":4,"role":"term"}])
    assert evidence["decision_status"] == "evidence-only" and not evidence["resolver_eligible"]
    print("Phase 9 Alpha 2.2 evidence-gating tests passed")


if __name__ == "__main__":
    main()
