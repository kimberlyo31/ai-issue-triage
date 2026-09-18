@isTest
private class TimeBasedEscalationStrategyTest {
    @isTest
    static void criticalIssueEscalatesPastFourHourSla() {
        TimeBasedEscalationStrategy strategy = new TimeBasedEscalationStrategy();

        GitHub_Issue__c stale = new GitHub_Issue__c(Severity__c = 'Critical', Opened_Date__c = System.now().addHours(-5));
        GitHub_Issue__c fresh = new GitHub_Issue__c(Severity__c = 'Critical', Opened_Date__c = System.now().addHours(-1));

        System.assertEquals(true, strategy.shouldEscalate(stale));
        System.assertEquals(false, strategy.shouldEscalate(fresh));
    }

    @isTest
    static void lowSeverityHasMuchLongerSla() {
        TimeBasedEscalationStrategy strategy = new TimeBasedEscalationStrategy();
        GitHub_Issue__c issueRecord = new GitHub_Issue__c(Severity__c = 'Low', Opened_Date__c = System.now().addHours(-5));

        System.assertEquals(false, strategy.shouldEscalate(issueRecord));
    }

    @isTest
    static void missingSeverityOrDateNeverEscalates() {
        TimeBasedEscalationStrategy strategy = new TimeBasedEscalationStrategy();
        System.assertEquals(false, strategy.shouldEscalate(new GitHub_Issue__c()));
    }
}
