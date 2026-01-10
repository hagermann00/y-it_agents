# PROOF & ASSEMBLY PROMPT

> Combines chapter prose with generated image paths. Final QC before formatting.

---

## PROMPT

Combine the chapter prose with the generated image manifest.

### TASK

1. **Replace** each `[IMAGE]...[/IMAGE]` block with:
   ```markdown
   ![caption](../images/ch{X}/{image_id}.png)
   *{caption text}*
   ```

2. **Verify**:
   - [ ] All [IMAGE] blocks resolved (none remaining)
   - [ ] All image paths exist in manifest
   - [ ] Captions match and are properly formatted
   - [ ] Flow reads naturally with images placed
   - [ ] PosiBot sidebars present (min per chapter spec)
   - [ ] Chad arc progression correct

3. **Flag issues** for human review:
   - Missing images
   - Placement concerns
   - Caption mismatches
   - Flow disruptions

### OUTPUT

- Complete chapter markdown with embedded image paths
- Issues list (if any)

---

## CHAPTER PROSE

```
[Paste Sonnet-generated chapter here]
```

---

## IMAGE MANIFEST

```json
[Paste extension output manifest.json here]
```

---

## ASSEMBLED OUTPUT:
