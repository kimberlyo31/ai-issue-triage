/**
 * Scheduled Apex can't make synchronous HTTP callouts, so
 * GitHubIssueTriageScheduler enqueues this Queueable to do the classification work.
 */
public class IssueClassificationQueueable implements Queueable, Database.AllowsCallouts {
    private AIProvider provider;
    private EscalationStrategy escalationStrategy;

    public IssueClassificationQueueable() {
        this(new AnthropicProvider(), new TimeBasedEscalationStrategy());
    }

    @TestVisible
    private IssueClassificationQueueable(AIProvider provider, EscalationStrategy escalationStrategy) {
        this.provider = provider;
        this.escalationStrategy = escalationStrategy;
    }

    public void execute(QueueableContext ctx) {
        List<GitHub_Issue__c> newIssues = [
            SELECT Id, Title__c, Body__c, Severity__c, Opened_Date__c, Status__c
            FROM GitHub_Issue__c
            WHERE Status__c = 'New'
            LIMIT 200
        ];
        if (newIssues.isEmpty()) {
            return;
        }
        new IssueClassificationService(provider, escalationStrategy).classifyAndRoute(newIssues);
    }
}
