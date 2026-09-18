@isTest
private class AnthropicProviderTest {
    @isTest
    static void parsesAClaudeMessagesResponseIntoAClassificationResult() {
        String responseBody = JSON.serialize(new Map<String, Object>{
            'content' => new List<Object>{
                new Map<String, Object>{
                    'type' => 'text',
                    'text' => JSON.serialize(new Map<String, Object>{
                        'category' => 'Bug',
                        'severity' => 'High',
                        'confidence' => 0.87,
                        'rationale' => 'Stack trace indicates a null reference on startup.'
                    })
                }
            }
        });

        ClassificationResult result = AnthropicProvider.parse(responseBody);

        System.assertEquals('Bug', result.category);
        System.assertEquals('High', result.severity);
        System.assertEquals(0.87, result.confidence);
    }
}
