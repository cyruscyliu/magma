<?php

class ExampleClass
{
    public const EXAMPLE_CONST = 42;
}

enum ExampleEnum: int
{
    case ENUM_CASE = ExampleClass::EXAMPLE_CONST;
}

var_dump(ExampleEnum::ENUM_CASE->value);

?>