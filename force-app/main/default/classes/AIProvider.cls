/**
 * Strategy interface for anything that can classify a GitHubIssue__c.
 */
public interface AIProvider {
    ClassificationResult classify(String title, String body);
}
