@isTest
private class IssueClassificationQueueableTest {
    @isTest
    static void enqueuedJobClassifiesAllNewIssues() {
        insert new GitHub_Issue__c(
            Title__c = 'App crashes on startup',
            Body__c = 'throws an exception and closes',
            Repo__c = 'demo/widgets',
            External_Number__c = 101,
            Status__c = 'New',
            Opened_Date__c = System.now()
        );

        Test.startTest();
        System.enqueueJob(new IssueClassificationQueueable(new MockAIProvider(), new TimeBasedEscalationStrategy()));
        Test.stopTest();

        List<GitHub_Issue__c> processed = [SELECT Status__c, Category__c FROM GitHub_Issue__c WHERE Status__c != 'New'];
        System.assertEquals(1, processed.size());
        System.assertEquals('Bug', processed[0].Category__c);
    }
}
