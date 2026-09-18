@isTest
private class IssueClassificationServiceTest {
    @isTest
    static void classifiesAndRoutesABugAsEngineeringAndEscalated() {
        GitHub_Issue__c issueRecord = new GitHub_Issue__c(
            Title__c = 'App crashes on startup',
            Body__c = 'throws an exception and closes immediately',
            Repo__c = 'demo/widgets',
            External_Number__c = 101,
            Status__c = 'New',
            Opened_Date__c = System.now().addHours(-10) // past the 4h Critical SLA
        );
        insert issueRecord;

        Test.startTest();
        new IssueClassificationService(new MockAIProvider(), new TimeBasedEscalationStrategy())
            .classifyAndRoute(new List<GitHub_Issue__c>{ issueRecord });
        Test.stopTest();

        GitHub_Issue__c updated = [
            SELECT Category__c, Severity__c, Team__c, Status__c, Is_Escalated__c
            FROM GitHub_Issue__c
            WHERE Id = :issueRecord.Id
        ];
        System.assertEquals('Bug', updated.Category__c);
        System.assertEquals('Critical', updated.Severity__c);
        System.assertEquals('Engineering', updated.Team__c);
        System.assertEquals(true, updated.Is_Escalated__c);
        System.assertEquals('Escalated', updated.Status__c);
    }

    @isTest
    static void freshLowSeverityIssueIsRoutedWithoutEscalation() {
        GitHub_Issue__c issueRecord = new GitHub_Issue__c(
            Title__c = 'Feature request: dark mode',
            Body__c = 'would be nice to have a dark theme',
            Repo__c = 'demo/widgets',
            External_Number__c = 103,
            Status__c = 'New',
            Opened_Date__c = System.now()
        );
        insert issueRecord;

        Test.startTest();
        new IssueClassificationService(new MockAIProvider(), new TimeBasedEscalationStrategy())
            .classifyAndRoute(new List<GitHub_Issue__c>{ issueRecord });
        Test.stopTest();

        GitHub_Issue__c updated = [SELECT Team__c, Status__c, Is_Escalated__c FROM GitHub_Issue__c WHERE Id = :issueRecord.Id];
        System.assertEquals('Product', updated.Team__c);
        System.assertEquals(false, updated.Is_Escalated__c);
        System.assertEquals('Routed', updated.Status__c);
    }
}
