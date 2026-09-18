/**
 * Scheduled entry point.
 * Schedule via: System.schedule('GitHub Issue Triage', '0 0 * * * ?', new GitHubIssueTriageScheduler());
 */
public class GitHubIssueTriageScheduler implements Schedulable {
    public void execute(SchedulableContext ctx) {
        System.enqueueJob(new IssueClassificationQueueable());
    }
}
