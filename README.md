## Documentations and Report : MVP of Circuit Designer MCP server.

### Below are some features any intelligence needs to design any circuit:
1. Understanding requirements
2. Knowledge of components
3. Circuit theory or design rules
4. Simulation & analysis skills and tools
5. Domain-specific knowledge

### For average LLMs, they have these capabilities:
1. Ability to understand requirements
2. Basic circuit theory and design rules
3. Simulation skills (how to simulate any circuit on any tool)

### In this MCP server, I’ve provided the tools missing in LLMs to mimic human intelligence and design circuits based on user requirements:
1. **Knowledge of Components**: `get_component_datasheet()` — fetches and converts component datasheet PDFs from manufacturers' websites into Markdown format (easy to understand for LLMs).
2. **Simulation Tools**: If the user has installed ngspice, it provides an interface to run simulation commands on netlist files and get the result.
3. **Domain-Specific Knowledge**: `get_research_paper()` — fetches research paper PDFs from the internet and converts them into Markdown.
4. **Basic instructions for LLMs** to understand the entire cycle of circuit generation.

### Technologies Used:
- **Language**: Python
- **Libraries**:
  - `duckduckgo_search`: for search queries
  - `requests`: for making HTTP requests
  - `fitz`: PDF processing library
  - `pymupdf4llm`: to convert PDF content into Markdown
  - `subprocess`: to run ngspice commands on the OS

## Report: Results from Using the MCP Server

*Note*: Due to my IT background, I am not proficient in judging it technically. I generated netlist code using Claude 3.7 Sonnet, with and without this MCP server, and compared the outputs using Claude itself. I selected a high-level topic for better comparability.

### Topic:
A 28 GHz mmWave RF front-end module for 6G communication, featuring low-noise amplification (NF ≤ 3.5 dB), high-efficiency power amplification (P_out ≥ 30 dBm), integrated T/R switching, and post-quantum encryption using a lattice-based cryptography core.

### Comparison Table

| Criteria                  | Without MCP Server                                                                 | With MCP Server                                                                 |
|--------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Component Specification  | 5/10 - Uses generic models without specific part numbers                           | 9/10 - Clearly specifies commercial parts with datasheets                      |
| Power Management         | 6/10 - Basic power distribution, limited isolation                                 | 9/10 - Multiple voltage domains, proper isolation                              |
| Signal Integrity         | 5/10 - Basic signal paths, limited impedance matching                              | 8/10 - Clearer signal chain, proper impedance considerations                   |
| Design Hierarchy         | 6/10 - Functional blocks defined, but overlapping                                  | 8/10 - Well-defined interfaces, functional separation                          |
| Testability              | 7/10 - Multiple analysis types, less focused on critical parameters               | 7/10 - Targeted analysis of key metrics, visual outputs                         |
| Documentation            | 6/10 - Basic documentation of components and purpose                              | 8/10 - Comprehensive documentation with expectations                           |
| Reproducibility          | 5/10 - Dependent on variable model parameters                                     | 9/10 - Uses standard components, consistent replication                        |
| Maintainability          | 5/10 - Less structured, hard to modify                                            | 8/10 - Segmented design, easy to modify                                       |
| Simulation Efficiency    | 5/10 - Complex models, convergence issues                                         | 8/10 - Simplified models for simulation speed                                  |
| Design Reusability       | 5/10 - Custom elements, limited portability                                       | 8/10 - Industry-standard components, reusable                                 |
| **TOTAL**                | **55/100 (55%)**                                                                  | **82/100 (82%)**                                                               |

### Summary Analysis
The "With MCP Server" netlist demonstrates superior circuit design practices across universal criteria, outperforming the "Without MCP Server" netlist by **27 points**, representing a **49.1% improvement**.

**Key advantages:**
- **Component Selection Strategy**: Uses real components with known specs for reliable implementation.
- **Hierarchical Design**: Clean modular structure eases debugging and upgrades.
- **Realistic Power Handling**: Correct voltage and current considerations ensure viability.
- **Simulation Practicality**: Speeds up analysis while retaining useful accuracy.
- **Enhanced Documentation**: Enables better collaboration and reuse.

### Known Issues
1. Fetching PDFs and converting to Markdown can be time-consuming — mitigated by limiting page count (first 2 pages usually contain essential info).
2. ngspice can’t simulate every component type.
3. The free tier of Claude-3.7 Sonnet can’t handle large examples like the one above due to token limits, but intermediate circuits work fine with curated prompts.
4. No schematic generation support yet.
5. `duckduckgo_search` is unofficial, but works well under usage limits.
6. Not optimal for basic circuits, which Claude can already generate well — MCP improves specification and realism.
7. If the prompt requirements are unclear, the MCP server may underperform compared to LLMs, as it relies heavily on real-world implementation, whereas LLMs tend to follow more theoretical approaches.
### Positive Highlights
1. Enhanced response quality for real-world implementations.
2. Excellent performance with detailed prompts.
3. Executes all relevant test cases and produces correct netlists.

### Future Enhancements
1. Bridging the gap between schematic design and netlist generation would create an outstanding combination.
2. Add interfaces for other simulation tools (based on user’s system setup).
3. Integrate component pricing and availability search.
4. Add web scraping tools to gather design insights and troubleshoot common issues.

---

My Point Of View:
The comparison results from Claude highlight the strong potential of this system. With dedicated research and development, it could become a valuable tool for users—capable of answering follow-up questions, suggesting optimizations, and predicting simulation outcomes. For example, it might recommend replacing component X with component Y to improve thermal resistance. While I haven't the expertise to evaluate its capabilities, I’ve made every effort to provide an unbiased perspective in this report.


