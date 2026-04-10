<?php

$strictlyAlphaNumeric = [
    "Az",
    "aZ",
    "A9",
    "a9",
    // Carrying values until the beginning of the string
    "Zz",
    "zZ",
    "9z",
    "9Z",
];

$strings = [
    // Empty string
    "",
    // String increments are unaware of being "negative"
    "-cc",
    // Trailing whitespace
    "Z ",
    // Leading whitespace
    " Z",
    // Non-ASCII characters
    "é",
    "あいうえお",
    "α",
    "ω",
    "Α",
    "Ω",
    // With period
    "foo1.txt",
    "1f.5",
    // With multiple period
    "foo.1.txt",
    "1.f.5",
];

foreach ($strictlyAlphaNumeric as $s) {
    var_dump(++$s);
}
foreach ($strings as $s) {
    var_dump(++$s);
}

// Will get converted to float on the second increment as it gets changed to a
// string interpretable as a number in scientific notation
$s = "5d9";
var_dump(++$s); // string(3) "5e0"
var_dump(++$s); // float(6)
?>