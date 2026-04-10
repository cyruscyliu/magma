<?php

print "Concat, which binds higher\n";

try {
    assert(false && foo() . bar() |> baz() . quux());
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

try {
    assert(false && (foo() . bar()) |> baz() . quux());
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

try {
    assert(false && foo() . (bar() |> baz()) . quux());
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

try {
    assert(false && foo() . bar() |> (baz() . quux()));
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

try {
    assert(false && (foo() . bar() |> baz()) . quux());
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

try {
    assert(false && foo() . (bar() |> baz() . quux()));
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

print "<, which binds lower\n";

try {
    assert(false && foo() < bar() |> baz());
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

try {
    assert(false && (foo() < bar()) |> baz());
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

try {
    assert(false && foo() < (bar() |> baz()));
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

try {
    assert(false && foo() |> bar() < baz());
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

try {
    assert(false && (foo() |> bar()) < baz());
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

try {
    assert(false && foo() |> (bar() < baz()));
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}



print "misc examples\n";

try {
    assert(false && foo() |> (bar() |> baz(...)));
} catch (AssertionError $e) {
    echo $e->getMessage(), PHP_EOL;
}

?>