/**
 * Strategy interface so escalation policy (SLA-based today) can be swapped
 * without touching classification or routing. 
 */
public interface EscalationStrategy {
    Boolean shouldEscalate(GitHub_Issue__c issueRecord);
}
