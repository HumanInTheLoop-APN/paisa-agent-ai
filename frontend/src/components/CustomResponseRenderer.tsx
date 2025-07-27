import React from 'react';
import { Markdown, ResponseRenderer } from '@nlux/react';
import { FinancialMetricsRenderer } from './response-renderers/FinancialMetricsRenderer';
import { ChartRenderer } from './response-renderers/ChartRenderer';
import { InvestmentRecommendationsRenderer } from './response-renderers/InvestmentRecommendationsRenderer';
import { DynamicFormRenderer } from './response-renderers/DynamicFormRenderer';

const isDynamicFormTool = (tool_results: any[]) => {
    return tool_results && tool_results[0].response.success && tool_results[0].response.form && tool_results[0].name === "dynamic_form_tool";
}

// Custom response renderer following NLUX documentation pattern
export const CustomResponseRenderer: ResponseRenderer<any> = (props) => {
    const { content, containerRef, serverResponse, } = props;

    console.log(">>> content", { content, containerRef, serverResponse });


    // Parse and render content based on type
    const renderContent = (content: any[]) => {
        return (
            <div className="response-container">
                {content.map((c, index) => {
                    return <>
                        {c.content && <Markdown key={index}>{c.content}</Markdown>}

                        {isDynamicFormTool(c.tool_results) &&
                            <div key={index}><DynamicFormRenderer data={c.tool_results[0].response.form} /></div>}
                    </>

                })}
            </div>
        );
    };

    if (!content) {
        return (
            <div className="response-container" ref={containerRef} />
        );
    }

    return (
        <div className="custom-response-renderer">
            {renderContent(content)}
        </div>
    );
}; 