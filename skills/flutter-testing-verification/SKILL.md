---
name: flutter-testing-verification
description: Write deterministic, fast unit tests, widget tests, golden tests, accessibility tests, and integration tests for Flutter and Dart applications using Fakes over Mocks, pumpApp harnesses, and WidgetTester. Use when adding test coverage, testing ViewModels/Notifiers/Repositories, verifying responsive UI across screen sizes, fixing flaky tests, or setting up E2E integration tests.
risk: safe
source: local
date_added: "2026-10-29"
---
# Flutter and Dart Testing and Verification Strategy

## Summary

Build reliable, deterministic tests across Unit, Widget, Golden/Accessibility, and Integration levels. Favor lightweight in-memory Fakes over brittle Mocks for application-owned repositories, inject deterministic clocks/dependencies, and verify every UI change across compact and expanded viewports.

## When to Use

- Writing unit tests for Repositories, Services, ViewModels, Notifiers, or Cubits
- Writing widget tests (`testWidgets`) to verify UI states (loading, empty, error, data) and user interactions
- Fixing flaky async tests (`pump` vs `pumpAndSettle`, fake timers, unclosed streams)
- Adding accessibility guideline assertions (`meetsGuideline`) or multi-viewport layout overflow checks
- Setting up E2E flows with `integration_test` or `patrol`

## Steps

### 1. Prefer Fakes Over Mocks for Owned Boundaries

Follow the official Flutter Architecture testing recommendation:

- **Create reusable `Fake<T>Repository` classes**: Implement your abstract `UserRepository` interface with an in-memory `FakeUserRepository` that stores a list/map and simulates configurable success or `AppFailure` responses. Fakes test real input/output contracts rather than brittle internal method call sequences.
- **When Mocks are needed**: For low-level third-party SDKs or verifying specific side-effect calls, use `mocktail` (zero codegen) or `mockito` (`@GenerateNiceMocks`).
- **Make time deterministic**: Never call `DateTime.now()` directly inside domain or ViewModel logic; use `clock.now()` from `package:clock` so unit tests can run inside `withClock(Clock.fixed(...), () { ... })`.

### 2. Write Thorough Unit Tests for Data and Logic Layers

Structure unit tests in `test/` mirroring the `lib/` folder path (`test/features/auth/ui/login_view_model_test.dart`):

- Follow the **Arrange - Act - Assert** structure inside descriptive `group()` and `test()` blocks.
- Test all branches of `Result<T>`: happy path data transformation, empty payload handling, network/server error mapping, and edge-case inputs.
- For Riverpod providers, create a scoped `ProviderContainer(overrides: [...])` with `addTearDown(container.dispose)` in a helper function.
- For Bloc/Cubit, use `blocTest<MyCubit, MyState>()` from `package:bloc_test` to assert state emission sequences cleanly.

### 3. Build a Reusable `pumpApp` Harness for Widget Tests

Eliminate boilerplate in `testWidgets` by creating a `pumpApp` extension on `WidgetTester` (see `references/test-harness-templates.md`):

- Wrap the widget under test in `MaterialApp` (including `localizationsDelegates`, `supportedLocales`, and `AppTheme.light`) and required DI providers (`ProviderScope` / `MultiBlocProvider`).
- **Find widgets by semantics, keys, or types**: Prefer `find.bySemanticsLabel(...)`, `find.text(...)`, `find.byKey(...)`, or `find.byType(...)` over fragile tree index lookups.
- **Understand `pump()` vs `pumpAndSettle()`**:
  - Use `await tester.pump()` to advance a single frame (e.g., to assert that a `CircularProgressIndicator` appears while an async request is pending).
  - Use `await tester.pumpAndSettle()` only when animations have finite completion. Calling `pumpAndSettle()` while an infinite indeterminate spinner (`CircularProgressIndicator`) is on screen will time out!

### 4. Test Responsive Breakpoints and Accessibility Guidelines

Catch layout overflows and a11y regressions automatically in widget tests:

- Test key screens at both compact phone width (`Size(375, 667)` with `textScaleFactor: 1.5`) and expanded tablet/desktop width (`Size(1024, 768)`) using `tester.view.physicalSize` and `addTearDown(tester.view.resetPhysicalSize)`.
- Run Flutter's built-in accessibility checks on critical screens:
  - `await expectLater(tester, meetsGuideline(androidTapTargetGuideline));`
  - `await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));`
  - `await expectLater(tester, meetsGuideline(textContrastGuideline));`

### 5. Run Verification Gates

Always run tests and static analysis before declaring a task complete:

```bash
flutter analyze
flutter test --randomize-ordering-seed=random
```

To collect test coverage and generate an `lcov.info` report:

```bash
flutter test --coverage
```

## Gotchas

- **`pumpAndSettle` timing out**: Almost always caused by an infinite animation (`CircularProgressIndicator`, shimmer skeleton, or repeating `AnimationController`). Use `await tester.pump(const Duration(milliseconds: 100))` instead.
- **HttpOverrides in widget tests**: By default, `flutter_test` blocks all real HTTP traffic and returns `400 Bad Request` for `Image.network`. Either wrap image loading behind an injectable image provider or use `mocktail_image_network` in widget tests.
- **Shared mutable state across tests**: Never share a mutable `FakeRepository` instance across multiple `test()` blocks without resetting it inside `setUp()`.

## Related Skills
- For a bug, write the failing reproduction before the fix. Do not re-run a clean green command when no code changed (`python-testing` Prove-It).
- Use **flutter-architecture-data** when testing repositories, services, or ViewModels.
- Use **flutter-state-management** when testing Notifiers, Cubits, or provider wiring.
- Use **dart-modern-idioms** when Dart async safety or pattern matching affects test structure.
- Use **verify-and-stop** for the decisive verification command before declaring completion.
- Use **flutter-performance-optimization** when frame-time or memory tests need dedicated performance assertions.
