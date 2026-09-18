/**
 * Classifies an issue via the Claude API through a Named Credential
 * Callouts happen from async context (Queueable/Schedulable) 
 */
public class AnthropicProvider implements AIProvider {
    private static final String NAMED_CREDENTIAL = 'callout:Anthropic_API';
    private static final String MODEL = 'claude-sonnet-5';

    private static final String SYSTEM_PROMPT =
        'You triage inbound software issues. Given a title and body, respond with ONLY a JSON object of the form: ' +
        '{"category": "Bug|Feature|Question|Documentation|Other", "severity": "Critical|High|Medium|Low", ' +
        '"confidence": 0.0-1.0, "rationale": "one sentence"}. No prose, no markdown fences, just the JSON object.';

    public ClassificationResult classify(String title, String body) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint(NAMED_CREDENTIAL + '/v1/messages');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setHeader('anthropic-version', '2023-06-01');
        req.setTimeout(20000);

        Map<String, Object> payload = new Map<String, Object>{
            'model' => MODEL,
            'max_tokens' => 300,
            'system' => SYSTEM_PROMPT,
            'messages' => new List<Map<String, Object>>{
                new Map<String, Object>{
                    'role' => 'user',
                    'content' => 'Title: ' + title + '\n\nBody:\n' + body
                }
            }
        };
        req.setBody(JSON.serialize(payload));

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() != 200) {
            throw new AIProviderException('Anthropic API returned ' + res.getStatusCode() + ': ' + res.getBody());
        }

        return parse(res.getBody());
    }

    @TestVisible
    private static ClassificationResult parse(String responseBody) {
        Map<String, Object> parsed = (Map<String, Object>) JSON.deserializeUntyped(responseBody);
        List<Object> content = (List<Object>) parsed.get('content');
        String rawText = '';
        for (Object block : content) {
            Map<String, Object> blockMap = (Map<String, Object>) block;
            if (blockMap.get('type') == 'text') {
                rawText += (String) blockMap.get('text');
            }
        }

        Map<String, Object> data = (Map<String, Object>) JSON.deserializeUntyped(rawText.trim());
        return new ClassificationResult(
            (String) data.get('category'),
            (String) data.get('severity'),
            (Decimal) data.get('confidence'),
            (String) data.get('rationale')
        );
    }

    public class AIProviderException extends Exception {}
}
