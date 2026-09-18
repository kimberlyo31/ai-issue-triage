public class MockAIProvider implements AIProvider {
    public ClassificationResult classify(String title, String body) {
        String text = ((title == null ? '' : title) + '\n' + (body == null ? '' : body)).toLowerCase();

        String category;
        if (text.contains('readme') || text.contains('documentation') || text.contains('typo')) {
            category = 'Documentation';
        } else if (text.contains('crash') || text.contains('exception') || text.contains('error') || text.contains('bug')) {
            category = 'Bug';
        } else if (text.contains('feature request') || text.contains('please add') || text.contains('enhancement')) {
            category = 'Feature';
        } else if (text.endsWith('?') || text.contains('how do i')) {
            category = 'Question';
        } else {
            category = 'Other';
        }

        String severity;
        if (text.contains('security') || text.contains('data loss') || text.contains('crash')) {
            severity = 'Critical';
        } else if (category == 'Bug') {
            severity = 'High';
        } else if (category == 'Feature') {
            severity = 'Low';
        } else {
            severity = 'Medium';
        }

        return new ClassificationResult(category, severity, 0.6, 'keyword match (mock provider)');
    }
}
