/**
 * Orchestrates classification -> routing -> escalation for a batch of
 * GitHub_Issue__c records. Takes its collaborators as constructor
 * parameters (AIProvider, EscalationStrategy) so callers can swap in
 * MockAIProvider for tests without any callout mocking.
 */
public class IssueClassificationService {
    private AIProvider provider;
    private EscalationStrategy escalationStrategy;

    public IssueClassificationService(AIProvider provider, EscalationStrategy escalationStrategy) {
        this.provider = provider;
        this.escalationStrategy = escalationStrategy;
    }

    public void classifyAndRoute(List<GitHub_Issue__c> issues) {
        for (GitHub_Issue__c issueRecord : issues) {
            ClassificationResult result = provider.classify(issueRecord.Title__c, issueRecord.Body__c);

            issueRecord.Category__c = result.category;
            issueRecord.Severity__c = result.severity;
            issueRecord.Confidence__c = result.confidence;
            issueRecord.Rationale__c = result.rationale;
            issueRecord.Team__c = IssueRouter.teamFor(result.category);

            Boolean escalate = escalationStrategy.shouldEscalate(issueRecord);
            issueRecord.Is_Escalated__c = escalate;
            issueRecord.Status__c = escalate ? 'Escalated' : 'Routed';
        }
        update issues;
    }
}
