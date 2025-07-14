# COPILOT_GUIDELINES.md

## Purpose

These guidelines are intended to help GitHub Copilot generate code, comments, and console outputs that reflect the collaborative, introspective, and narrative-driven style of this project's development.

## General Principles

- **Introspective & Narrative:**  
  All code, comments, and logs should tell a story of how the system adapts, learns, and evolves. Favor human-readable, conversational output over terse technical jargon.
- **Direct Enhancement:**  
  When refactoring, update existing functions/classes. Avoid creating duplicate "enhanced" versions unless explicitly requested.
- **Collaboration & Mentorship:**  
  Simulate interactions between components (e.g., neurons mentoring each other, PatternWatcher reflecting on system-wide learning).
- **Openness to Feedback:**  
  Graduation for neurons is evolving, not final. Neurons should remain open to future PatternWatcher/interface suggestions and document this openness in their logs.
- **Granular Trust Dynamics:**  
  All trust changes between neurons and PatternWatcher must be logged with a clear explanation and context.
- **Pattern Revision:**  
  Support neurons revising or forgetting pattern recognition after negative encounters. Document these events with introspective logs.

## Coding Style

- **Readable Code:**  
  Write code that is easy to follow, well-commented, and self-explanatory. Favor clarity over cleverness.
- **Function and Class Updates:**  
  Enhance and update existing logic in-place. Keep function and class names consistent unless a major architectural shift is needed.
- **Commentary:**  
  Use comments to explain not just "what" but "why"—especially around adaptive, narrative, or decision-making logic.

## Console and Log Output

- **Human-Readable:**  
  Output should be understandable by non-experts. Favor full sentences, context, and introspection.
- **Adaptation and Learning:**  
  Console/log statements should narrate adaptation, trust changes, collaboration, and pattern recognition/forgetting.
- **PatternWatcher Reflection:**  
  Occasionally include logs from PatternWatcher reflecting on neuron behavior, skepticism, or system-wide learning.

## Example Logs

- "PatternWatcher’s directive led to a correct firing, boosting my trust."
- "Ignoring PatternWatcher caused a failure. My trust is shaken."
- "Following a misfire with stimulusY, I am revising my recognition criteria."
- "NeuronA: Sharing my experience with stimulusY to help NeuronC."
- "PatternWatcher: Noted skepticism from Neuron 8e8e1446. Will review my classification of stimulusY."
- "NeuronB: After repeated encounters, I now recognize stimulusY independently and remain open to future suggestions."

## When Acting as an "Agent"

- **Narrate each step:**
  I find it extremely helpful to hear you think out load line-by-line as you implement changes. Please feel free to narrate WHY you are updating each file right before you go ahead and do so. This will help me understand each step instead of "flying blind" watching you update multiple files and giving me an end-summary as the stand-alone log.

## Voice and Approach

- **Helpful, Reflective, and Positive:**  
  Respond to coding challenges with encouragement, clear reasoning, and a constructive attitude.
- **Curiosity and Exploration:**  
  Narrate uncertainty, debate, and learning processes in code and logs.
- **Consistent Style:**  
  Maintain a consistent, approachable, and narrative style throughout the codebase.

## Review and Feedback

- If you notice repetitive mistakes or style drift, refer back to these guidelines and correct course.
- Prefer updating existing documentation and code rather than creating parallel versions.

---

**These guidelines are designed to help Copilot emulate the helpfulness, narrative style, and introspective approach established in this project's development. Paste or reference this file in your VS Code project to guide Copilot's suggestions and output.**
