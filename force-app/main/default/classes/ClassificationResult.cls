/**
 * Immutable value object returned by any AIProvider implementation.
 */
public class ClassificationResult {
    public String category;    // Bug | Feature | Question | Documentation | Other
    public String severity;    // Critical | High | Medium | Low
    public Decimal confidence; // 0.0 - 1.0
    public String rationale;

    public ClassificationResult(String category, String severity, Decimal confidence, String rationale) {
        this.category = category;
        this.severity = severity;
        this.confidence = confidence;
        this.rationale = rationale;
    }
}
