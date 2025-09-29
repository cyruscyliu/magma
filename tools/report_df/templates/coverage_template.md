{% extends base_template %}
{% block title -%}
Coverage summary
{%- endblock %}

{% block body %}
<div class="section">
    <h1>Coverage summary</h1>
    <p>
        This page summarizes the coverage data collected during fuzzing. In Magma v1.3 this feature 
        is enabled for 3 fuzzers AFL++, Honggfuzz and libFuzzer. For each target and its programs,
        <ol>
            <li>The overall percentage of branches covered</li>
            <li>The overall number of branches covered</li>
            <li>The percentage of branches covered measured over time</li>
            <li>The number of branches covered measured over time</li>      
        </ol>
        is plotted to compare the fuzzers. This data is combined across all trials in a 
        campaign. In addition to the plots, the source code coverage reports for each fuzzing 
        trial are listed.
    </p>
{% for target in cov_data%}
    <h2>{{ target }}</h2>
    {% for program in cov_data[target] %}
        {% set program_data = cov_data[target][program] %}
        <h3>{{ program }}</h3>
        <div class="row">
            <div class="col s6">{{ program_data['fig_percent'] }}</div>
            <div class="col s6">{{ program_data['fig_covered'] }}</div>
        </div>
        <div class="row">
             <div class="col s6">{{ program_data['fig_percent_overtime'] }}</div>
            <div class="col s6">{{ program_data['fig_covered_overtime'] }}</div>
        </div>
        <ul class="browser-default">
            {% for cov_link in program_data['links'] %}
                <li>{{cov_link}}</li>
            {% endfor %}
        </ul>
    {% endfor %}
{% endfor%}
</div>
{% endblock %}