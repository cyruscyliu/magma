<?php

require_once __DIR__ . DIRECTORY_SEPARATOR . 'test_offset_helpers.inc';

echo 'read op', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
$r = $o['foo'];
exportObject($o);

echo 'write op', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
$o['foo'] = true;
exportObject($o);

echo 'read-write op', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
$o['foo'] += 10;
exportObject($o);

echo 'isset op', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
$r = isset($o['foo']);
exportObject($o);

echo 'empty op', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
$r = empty($o['foo']);
exportObject($o);

echo 'null coalescing op', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
$r = $o['foo'] ?? 'default';
exportObject($o);

echo 'appending op', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
$o[] = true;
exportObject($o);

echo 'unset op', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
unset($o['foo']);
exportObject($o);

echo 'nested read', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
$r = $o['foo']['bar'];
exportObject($o);

// Illegal
//echo 'nested read: appending then read', PHP_EOL;
//$o = new DimensionHandlersNoArrayAccess();
//try {
//    $r = $o[]['bar'];
//} catch (\Throwable $e) {
//    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
//}

echo 'nested write', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $o['foo']['bar'] = true;
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

echo 'nested write: appending then write', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $o[]['bar'] = true;
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

echo 'nested read-write', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $o['foo']['bar'] += 10;
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

echo 'nested read-write: appending then write', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $o[]['bar'] += 10;
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

echo 'nested isset', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $r = isset($o['foo']['bar']);
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

// Illegal
//echo 'nested isset: appending then read', PHP_EOL;
//try {
//    $o = new DimensionHandlersNoArrayAccess();
//    $r = isset($o[]['bar']);
//} catch (\Throwable $e) {
//    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
//}
//exportObject($o);

echo 'nested empty', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $r = empty($o['foo']['bar']);
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

// Illegal
//echo 'nested empty: appending then read', PHP_EOL;
//try {
//    $o = new DimensionHandlersNoArrayAccess();
//    $r = empty($o[]['bar']);
//} catch (\Throwable $e) {
//    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
//}
//exportObject($o);

echo 'nested null coalescing', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $r = $o['foo']['bar'] ?? 'default';
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

// Illegal
//echo 'nested null coalescing: appending then read', PHP_EOL;
//try {
//    $o = new DimensionHandlersNoArrayAccess();
//    $r = $o[]['bar'] ?? 'default';
//} catch (\Throwable $e) {
//    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
//}
//exportObject($o);

echo 'nested appending', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $o['foo'][] = true;
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

echo 'nested appending: appending then append', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $o[][] = true;
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

echo 'nested unset', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    unset($o['foo']['bar']);
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

// Illegal
//echo 'nested unset: appending then read', PHP_EOL;
//try {
//    $o = new DimensionHandlersNoArrayAccess();
//    unset($o[]['bar']);
//} catch (\Throwable $e) {
//    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
//}
//exportObject($o);

echo 'reference fetching', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $r = &$o['foo'];
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

echo 'nested reference fetching', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $r = &$o['foo']['bar'];
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

echo 'reference fetch-append', PHP_EOL;
$o = new DimensionHandlersNoArrayAccess();
try {
    $r = &$o[];
} catch (\Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
exportObject($o);

?>