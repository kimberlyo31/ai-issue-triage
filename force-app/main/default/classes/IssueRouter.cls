/**
 * Category -> owning team.
 */
public class IssueRouter {
    @TestVisible
    private static final Map<String, String> TEAM_BY_CATEGORY = new Map<String, String>{
        'Bug' => 'Engineering',
        'Feature' => 'Product',
        'Question' => 'Support',
        'Documentation' => 'Docs',
        'Other' => 'Triage'
    };

    public static String teamFor(String category) {
        return TEAM_BY_CATEGORY.containsKey(category) ? TEAM_BY_CATEGORY.get(category) : 'Triage';
    }
}
