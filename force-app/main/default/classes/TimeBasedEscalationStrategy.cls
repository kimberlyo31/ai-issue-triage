/**
 * Escalates when an issue has been open longer than its severity's SLA.
 */
public class TimeBasedEscalationStrategy implements EscalationStrategy {
    @TestVisible
    private static final Map<String, Integer> SLA_HOURS_BY_SEVERITY = new Map<String, Integer>{
        'Critical' => 4,
        'High' => 24,
        'Medium' => 72,
        'Low' => 168
    };

    public Boolean shouldEscalate(GitHub_Issue__c issueRecord) {
        if (issueRecord.Severity__c == null || issueRecord.Opened_Date__c == null) {
            return false;
        }
        Integer slaHours = SLA_HOURS_BY_SEVERITY.get(issueRecord.Severity__c);
        if (slaHours == null) {
            return false;
        }
        Long ageInHours = (System.now().getTime() - issueRecord.Opened_Date__c.getTime()) / (1000 * 60 * 60);
        return ageInHours > slaHours;
    }
}
