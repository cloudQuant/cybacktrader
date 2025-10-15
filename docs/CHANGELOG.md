# Changelog

All notable changes to cybacktrader will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure with Cython support
- Compatibility layer for seamless migration from backtrader
- Cython-optimized `mathsupport` module
- Comprehensive documentation:
  - README.md with quick start guide
  - MIGRATION_GUIDE.md for users
  - PERFORMANCE.md with benchmark results
  - CONTRIBUTING.md for developers
- Setup configuration for Cython compilation
- Migration script for batch updating imports
- Baseline benchmark suite

### Changed
- Package structure to support both Python and Cython modules
- Build system to use setuptools with Cython extensions

### Performance
- `mathsupport` module: ~1.15x speedup with Cython optimization
- Overall framework: ~1.15x speedup (兼容层模式)
- Target: 10x+ speedup after full optimization

## [0.1.0] - 2025-10-14

### Added
- Initial release
- Full API compatibility with backtrader
- Basic Cython infrastructure
- Test suite migration tools

### Architecture
- Hybrid approach: Cython modules with Python fallback
- Progressive optimization strategy
- Priority-based module conversion:
  - Priority A: Core data path (linebuffer, lineiterator, lineseries)
  - Priority B: Compute-intensive (indicators, mathsupport)
  - Priority C: Orchestration (cerebro, broker, order)

### Documentation
- Project README
- Migration guide
- Performance analysis
- Contributing guidelines

## Roadmap

### Version 0.2.0 (Target: Q1 2025)
- [ ] Cythonize core line modules (linebuffer, lineiterator, lineseries)
- [ ] Expected performance: 3-5x speedup
- [ ] Comprehensive benchmark suite
- [ ] Memory usage optimization

### Version 0.3.0 (Target: Q2 2025)
- [ ] Cythonize indicator base classes
- [ ] Optimize top 10 most-used indicators (SMA, EMA, RSI, MACD, etc.)
- [ ] Expected performance: 5-8x speedup
- [ ] Advanced profiling tools

### Version 0.5.0 (Target: Q3 2025)
- [ ] Cythonize cerebro and broker modules
- [ ] Parallel execution improvements
- [ ] Expected performance: 8-10x speedup
- [ ] Production-ready release

### Version 1.0.0 (Target: Q4 2025)
- [ ] Full feature parity with backtrader
- [ ] 10x+ performance improvement
- [ ] Comprehensive test coverage (>90%)
- [ ] Production battle-tested
- [ ] Complete documentation

## Performance Milestones

| Version | Target Speedup | Status |
|---------|---------------|--------|
| 0.1.0 | 1.15x | ✅ Achieved |
| 0.2.0 | 3-5x | 📋 Planned |
| 0.3.0 | 5-8x | 📋 Planned |
| 0.5.0 | 8-10x | 📋 Planned |
| 1.0.0 | 10x+ | 🎯 Goal |

## Breaking Changes

None yet. We are committed to maintaining 100% API compatibility with backtrader.

## Deprecations

None yet.

## Known Issues

- [ ] Cython modules require C compiler (platform-specific)
- [ ] Windows requires Visual Studio Build Tools
- [ ] Some advanced features not yet optimized

## Contributors

Thank you to all contributors who helped make cybacktrader possible!

- [Your Name] - Project Lead

## License

This project maintains the same license as backtrader.

---

For more details, see the [commit history](https://github.com/yourusername/cybacktrader/commits/main).

