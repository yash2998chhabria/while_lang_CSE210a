@test "test-1" {
  check 'if x > 5 then x := 1 else z := 1; while y < 1 do y := 1' '{y → 1, z → 1}'
}
@test "test-2" {
  check 'if ¬ (1 - 1  < 0) then z8 := 09 else z3 := 90' '{z8 → 9}'
}
@test "test-3" {
  check 'if ( true ∧ false ) then p := t else p := t + 1' '{p → 1}'
}
@test "test-4" {
  check 'x := y - - - -3 + t - + -2' '{x → 5}'
}
@test "test-5" {
  check 'if ¬ true then x := 1 else {skip; k := -2}' '{k → -2}'
}
