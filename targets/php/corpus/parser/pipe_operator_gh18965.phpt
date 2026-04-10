<?php
namespace Foo;
range(0, 10) |> assert(...);
echo "No leak\n";
?>