# Inference Theorem

## Informal statement

Given `n` input files that belong to the same family and share a similar underlying data structure, an agent can induce a common semantic backbone from those files.

This semantic backbone is independent from the concrete representation format of the original files.

The original files may be HTML, Markdown, CSV, JSON, XML, plain text, logs, PDFs, or another structured/semi-structured representation. The important condition is not that the files use the same surface syntax, but that they express instances of the same underlying information structure.

From this induced backbone, the agent can derive extraction fingerprints that target the concrete representation of each source format.

Therefore, the process has two layers:

1. **Semantic induction**: infer the data structure semantics shared by the inputs.
2. **Representation targeting**: infer how each semantic field is located inside a concrete file representation.

Together, these allow a later extractor to transform sibling files into normalized JSON.

---

## Core idea

Information does not have a single universal representation.

The same information may appear as:

- HTML
- JSON
- CSV
- Markdown
- XML
- plain text
- a database row
- a document
- an API response

However, different representations may still encode the same underlying semantic structure.

For example, a profile page may contain:

- name
- introduction
- experience
- commentaries

The HTML tags are not the information itself. They are one possible surface representation of the information.

The semantic structure underneath is the backbone.

---

## Data Structure Semantics

The first artifact produced by induction is the **Data Structure Semantics**.

This is the representation-independent schema of the information contained in the input family.

It describes:

- field names
- primitive types
- composite types
- nesting
- cardinality
- optionality
- semantic meaning

It does not describe where the data is found in a concrete file.

That belongs to the fingerprint layer.

---

## Type model

All semantic fields are represented as objects so that metadata can be attached uniformly.

There are two categories of types:

1. **Leaf types**
2. **Composite types**

### Leaf types

Leaf types are primitive values.

Supported leaf types:

| Symbol | Meaning |
| --- | --- |
| `s` | string |
| `b` | boolean |
| `i` | integer |
| `f` | float |

A leaf field is represented as:

```json
{
  "name": {
    "type": "s"
  }
}
```

By default, fields should be treated as optional unless the induction process has a strong reason to mark them as invariant.

This means `required: true` should be used carefully.

The absence of a field in a future sibling file should not automatically invalidate the extraction unless the manifest explicitly declares that field as required.

### Composite types

Composite types contain other types.

There are two kinds of composites:

1. **Shared-type composites**
2. **Custom-type composites**

A shared-type composite is a composite whose contained elements all share the same type.

A custom-type composite is a composite whose contained elements may have different field/type structures.

Supported composite symbols:

| Symbol | Meaning |
| --- | --- |
| `array<T>` | ordered collection where all items share type `T` |
| `object<T>` | keyed structure where all values share type `T` |
| `array<N>` | ordered collection with non-uniform/custom item types |
| `object<N>` | keyed structure with non-uniform/custom field types |

The `T` symbol means the composite contains a shared repeated type.

The `N` symbol means the composite contains non-uniform or named custom types.

### Shared-type array

A shared-type array is represented with `type: "array<T>"` and an `item` definition.

```json
{
  "experience": {
    "type": "array<T>",
    "item": {
      "type": "s"
    }
  }
}
```

### Shared-type object

A shared-type object is represented with `type: "object<T>"` and an `item` definition.

This is useful when the object keys vary, but all values share the same structure.

```json
{
  "metrics": {
    "type": "object<T>",
    "item": {
      "type": "f"
    }
  }
}
```

This could represent data like:

```json
{
  "metrics": {
    "height": 1.82,
    "weight": 75.5,
    "score": 98.2
  }
}
```

### Custom-type array

A custom-type array is represented with `type: "array<N>"` and an `items` list.

This is useful when the array positions or members do not all share the same type.

```json
{
  "sections": {
    "type": "array<N>",
    "items": [
      {
        "type": "object<N>",
        "fields": {
          "title": {
            "type": "s"
          }
        }
      },
      {
        "type": "object<N>",
        "fields": {
          "body": {
            "type": "s"
          }
        }
      }
    ]
  }
}
```

### Custom-type object

A custom-type object is represented with `type`: `"object<N>"` and a `fields` definition.

This is useful when the object has named fields with different types.

```json
{
  "commentary": {
    "type": "object<N>",
    "fields": {
      "text": {
        "type": "s"
      },
      "author": {
        "type": "s"
      },
      "likes": {
        "type": "i"
      }
    }
  }
}
```

An array of custom objects is represented as a shared-type array whose repeated item is a custom object.

```json
{
  "commentaries": {
    "type": "array<T>",
    "item": {
      "type": "object<N>",
      "fields": {
        "text": {
          "type": "s"
        },
        "author": {
          "type": "s"
        }
      }
    }
  }
}
```

---

## Set-theoretic view of induction

Let each input file expose a set of semantic properties.

For input files:

$$
I_1, I_2, ..., I_n
$$

Let the semantic properties observed in each file be:

$$
P(I_1), P(I_2), ..., P(I_n)
$$

The induced semantic backbone should usually be the union of observed properties:

$$
S = \bigcup_{k=1}^{n} P(I_k)
$$

This means the semantic schema should capture the fullest observed picture across sibling files.

A property that appears in only one input is still part of the possible semantic structure of the family.

The intersection can be useful, but it should not be confused with the full schema:

$$
C = \bigcap_{k=1}^{n} P(I_k)
$$

Where:

- $S$ = complete observed semantic set
- $C$ = common observed semantic core

Fields in $C$ are stronger candidates for invariants.

Fields in $S - C$ are outsider or variant properties.

Therefore, the default rule is:

```txt
All fields are optional unless promoted to invariant by evidence or by explicit declaration.
```

This avoids overfitting the extractor to the limited sample of input files.

---

## Example Data Structure Semantics

For a family of profile-like documents, the induced semantic backbone may be:

```json
{
  "schema_name": "profile",
  "type": "object<N>",
  "fields": {
    "name": {
      "type": "s",
      "required": false,
      "description": "The name of the profile entity."
    },
    "introduction": {
      "type": "s",
      "required": false,
      "description": "A short introductory description of the profile entity."
    },
    "experience": {
      "type": "array<T>",
      "required": false,
      "item": {
        "type": "s"
      },
      "description": "A list of experience entries."
    },
    "commentaries": {
      "type": "array<T>",
      "required": false,
      "item": {
        "type": "object<N>",
        "fields": {
          "text": {
            "type": "s",
            "required": true
          },
          "author": {
            "type": "s",
            "required": false
          }
        }
      },
      "description": "A list of commentaries associated with the profile."
    }
  }
}
```

This artifact says what the data is.

It does not yet say where the data lives.

---

## Extraction Fingerprint

The second artifact produced by induction is the **Extraction Fingerprint**.

The fingerprint maps the representation-independent semantic backbone to the concrete structure of a file format.

For HTML, the fingerprint may contain DOM selectors, semantic anchors, headings, fallback routes, and normalization rules.

For CSV, it may contain column mappings.

For JSON, it may contain JSON paths.

For XML, it may contain XPath expressions.

For Markdown, it may contain heading anchors and section rules.

The fingerprint is representation-specific.

The semantic backbone is representation-independent.

---

## HTML fingerprint example

Given the semantic field `name`, the HTML fingerprint may say:

```json
{
  "field": "name",
  "target": {
    "format": "html",
    "strategy": "css_selector",
    "selector": "main.profile-card > h1.person-name",
    "attribute": "textContent"
  },
  "normalizers": ["trim", "collapse_whitespace"],
  "confidence": 0.98
}
```

A more semantic target may say:

```json
{
  "field": "experience",
  "target": {
    "format": "html",
    "strategy": "section_by_heading",
    "root": "main.profile-card",
    "heading": "Experience",
    "item_selector": "li",
    "attribute": "textContent"
  },
  "cardinality": "many",
  "normalizers": ["trim", "collapse_whitespace"],
  "confidence": 0.94
}
```

The fingerprint should prefer semantic anchors over brittle absolute paths.

For example, prefer:

```json
{
  "strategy": "section_by_heading",
  "heading": "Experience",
  "item_selector": "li"
}
```

Instead of:

```json
{
  "strategy": "css_selector",
  "selector": "body > main > section:nth-child(3) > ul > li"
}
```

---

## Source-to-Target Manifest

The complete induction output can be called a **Source-to-Target Manifest**.

It contains both:

1. The Data Structure Semantics
2. The Extraction Fingerprint

The manifest is the contract between induction and extraction.

A later extractor should be able to receive only:

```txt
source file + source-to-target manifest
```

And produce:

```txt
normalized JSON + extraction report
```

The extractor should not need access to the original induction examples.

This is where the context can be cut.

The induction agent reads the original examples and produces the manifest.

A later script-generation agent should not need to reread the original files if the manifest is complete enough.

It should be able to read only:

```txt
semantics + fingerprint
```

And generate an executable scraper/extractor.

For an HTML family, that generated extractor may be a Python script using a DOM-capable parser such as BeautifulSoup.

The extractor then becomes a function from one representation into another:

$$
s : \langle name \rangle.html \rightarrow \langle name \rangle.json
$$

Or more generally:

$$
s_R : X_R \rightarrow J
$$

Where:

- $s_R$ = scraper/extractor for representation family $R$
- $X_R$ = an input file belonging to representation family $R$
- $J$ = normalized JSON output

The practical contract is:

```txt
input:  <name>.html
output: <name>.json
```

The output file should preserve the input file identity while changing only the representation.

---

## Manifest example

```json
{
  "manifest_version": "1.0",
  "family": "profile_documents",
  "semantics": {
    "schema_name": "profile",
    "type": "object<N>",
    "fields": {
      "name": {
        "type": "s",
        "required": false
      },
      "introduction": {
        "type": "s",
        "required": false
      },
      "experience": {
        "type": "array<T>",
        "required": false,
        "item": {
          "type": "s"
        }
      },
      "commentaries": {
        "type": "array<T>",
        "required": false,
        "item": {
          "type": "object<N>",
          "fields": {
            "text": {
              "type": "s",
              "required": true
            },
            "author": {
              "type": "s",
              "required": false
            }
          }
        }
      }
    }
  },
  "fingerprint": {
    "format": "html",
    "root": {
      "strategy": "css_selector",
      "selector": "main.profile-card"
    },
    "fields": {
      "name": {
        "strategy": "css_selector",
        "selector": "main.profile-card > h1.person-name",
        "attribute": "textContent",
        "normalizers": ["trim", "collapse_whitespace"],
        "confidence": 0.98
      },
      "introduction": {
        "strategy": "section_by_heading",
        "heading": "Introduction",
        "value_selector": "p",
        "attribute": "textContent",
        "normalizers": ["trim", "collapse_whitespace"],
        "confidence": 0.95
      },
      "experience": {
        "strategy": "section_by_heading",
        "heading": "Experience",
        "item_selector": "li",
        "attribute": "textContent",
        "cardinality": "many",
        "normalizers": ["trim", "collapse_whitespace"],
        "confidence": 0.94
      },
      "commentaries": {
        "strategy": "section_by_heading",
        "heading": "Commentaries",
        "item_selector": "article.comment",
        "cardinality": "many",
        "fields": {
          "text": {
            "selector": "p",
            "attribute": "textContent",
            "normalizers": ["trim", "collapse_whitespace"]
          },
          "author": {
            "selector": ".author",
            "attribute": "textContent",
            "normalizers": ["trim", "collapse_whitespace"]
          }
        },
        "confidence": 0.91
      }
    }
  }
}
```

---

## The theorem

If a set of `n` input files share a stable underlying data structure, then an agent can induce a representation-independent semantic backbone from those inputs.

The induced backbone should be modeled as the union of observed semantic properties, not merely the intersection.

$$
S = \bigcup_{k=1}^{n} P(I_k)
$$

The common core is still useful:

$$
C = \bigcap_{k=1}^{n} P(I_k)
$$

But the common core $C$ should be treated as the set of likely invariants, while the full semantic backbone $S$ should include variant properties as well.

If the source representation contains stable anchors for the semantic fields, the agent can also induce a representation-specific extraction fingerprint.

Therefore, a source-to-target manifest can be constructed such that a later extractor can transform unseen sibling files into normalized JSON without access to the original examples.

In symbolic form:

```txt
I₁, I₂, ..., Iₙ  →  S
```

Where:

- `I` = input file
- `S` = induced data structure semantics

Then:

```txt
S + R  →  F
```

Where:

- `R` = source representation family
- `F` = extraction fingerprint

And finally:

```txt
X + S + F  →  J
```

Where:

- `X` = unseen sibling input file
- `J` = normalized JSON output

For file-producing extractors:

$$
s_R(X_R) = J
$$

And in the HTML case:

$$
s_{html}(\langle name \rangle.html) = \langle name \rangle.json
$$

## Reasoning phases

### 1. Induction

The agent observes multiple examples and infers the shared semantic structure.

```txt
examples → semantics
```

### 2. Fingerprinting

The agent maps semantic fields to representation-specific extraction targets.

```txt
semantics + source representation → fingerprint
```

### 3. Program synthesis

The agent generates an extractor from the manifest.

```txt
manifest → extractor
```

### 4. Deductive application

The extractor applies the induced rules to an unseen sibling file.

```txt
new input + extractor → JSON
```

---

## Design principle

The induction layer should be intelligent.

The extraction layer should be deterministic.

The extractor should not rediscover the structure every time.

It should only apply the already-induced manifest.

This creates a separation of responsibilities:

```txt
Inducer: examples → manifest
Generator: manifest → extractor
Extractor: input → JSON
Validator: JSON → report
```

---

## Practical rule

Do not make the extractor depend on hidden context.

Every field should carry its own extraction target.

Every composite should define how its children are reached.

Every repeated structure should define its item target.

Every output should be validated against the induced semantics.

This makes the system stateless, inspectable, and portable.