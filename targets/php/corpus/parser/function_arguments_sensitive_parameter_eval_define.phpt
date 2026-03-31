<?php

eval(<<<'EOT'
function test(#[SensitiveParameter] $sensitive)
{
    debug_print_backtrace();
    var_dump(debug_backtrace());
    var_dump((new Exception)->getTrace());
}
EOT);

test('sensitive');

?>