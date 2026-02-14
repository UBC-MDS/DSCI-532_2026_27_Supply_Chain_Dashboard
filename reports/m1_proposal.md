# Supply Chain Dashboard Proposal

## Section 1: Motivation and Purpose

> **Our role:** Data Science Consultancy Firm
> **Target audience:** Supply Chain Managers for Beauty Retailers
>
> In many industries, such as the Beauty retail industry, it is important to monitor the flow of goods and services going in and out of organizations. When a supply chain is inefficient, there are quality control issues, overstocking/understocking, excessive costs etc. Monitoring these factors would allow companies to optimize their management resulting in more efficiency such as minimizing costs and maximizing profits. To make this possible, we propose to build a data visualization app that allows supply chain managers to identify revenue generated based on product categories, number of products sold, customer demographics etc. These different factors would allow retailers, specifically Beauty Retailers to make meaningful business decisions based on which products perform well and also identifying areas where they can improve upon or cut costs with the motivation to generate more profit and improve customer satisfaction.


## Section 2: Description of the Data

> We will be visualizing a dataset of 100 records from a Fashion and Beauty startup with 24 different variables that contain the following supply chain information, which we hypothesize could be helpful for improving supply chain efficiency. This dataset contains a mix of numeric and categorical variables, allowing us to create a wide variety of visualizations depending on the information we want to convey per visualization. The categories include:
>
> - Categories (`Product type`, `Customer Demographics`, `Location`, `Supplier Name`)
> - Prices and Expenses (`Price`, `Costs`, `Revenue Generated` etc.)
> - Product Movement (`Availability`, `Number of Products sold`, `Stock levels`)
> - Quality Control (`Inspection Results`, `Defect rates`)
>
> Using variables such as the ones mentioned can also be used to derive new columns, for example we can get the `Cost per unit` by dividing `Costs` by `Number of Products sold`. We can also group by different categories, for example we can look at `Defect rates` based on `Location`.

## Section 3: Research Questions & Usage Scenarios

### Persona
JacK Ma is a Supply Chain Manager at a mid-sized fashion and beauty company operating across multiple cities in India. She oversees inventory planning, vendor relationships, and logistics optimization. Her quarterly reports to executive leadership require data-driven insights on cost reduction opportunities and operational bottlenecks.

### Usage Scenario
Jack is preparing for her Q1 performance review and needs to identify why shipping costs spiked 18% last quarter despite relatively stable sales volumes. She opens the Supply Chain Analytics Dashboard to investigate patterns across transportation modes, routes, and carriers. She wants to compare shipping costs against delivery times to determine if the company is overpaying for expedited shipping when standard routes would suffice. Additionally, she needs to identify which suppliers have the highest defect rates to renegotiate contracts or find alternatives. By filtering data by location, product type, and time periods, she can build a compelling case for optimizing carrier selection and supplier partnerships.

### User Stories

**User Story 1:**
As a supply chain manager, I want to filter shipments by transportation mode and route so that I can identify the most cost-effective shipping methods for different product types.

**User Story 2:**
As a supply chain manager, I want to compare defect rates across suppliers and locations so that I can prioritize quality improvement initiatives and supplier negotiations.

**User Story 3:**
As a supply chain manager, I want to visualize the relationship between lead times and stock levels so that I can optimize inventory reorder points and reduce stockout risks.

### Jobs to Be Done

**JTBD 1:**
**Situation:** When reviewing quarterly cost reports...
**Motivation:** ...I need to separate routine shipping expenses from outlier high-cost shipments...
**Outcome:** ...so that I can investigate root causes of cost overruns.

**JTBD 2:**
**Situation:** When evaluating supplier performance...
**Motivation:** ...I need to correlate defect rates with manufacturing costs and production volumes...
**Outcome:** ...so that I can assess whether premium suppliers deliver proportional quality value.

**JTBD 3:**
**Situation:** When planning inventory levels...
**Motivation:** ...I need to identify patterns in lead time variability across locations and suppliers...
**Outcome:** ...so that I can set appropriate safety stock levels for each product category.

## Section 4: Exploratory Data Analysis

To validate User Story 1 (filtering shipments by transportation mode to identify cost-effective options), we analyzed the relationship between shipping costs, delivery times, and transportation modes in the supply chain dataset.

Our analysis reveals distinct cost-time profiles across the four transportation modes:

| Transportation Mode | Avg Cost | Avg Time (days) | Sample Size |
|---------------------|----------|-----------------|-------------|
| Air                 | $6.02    | 5.12            | 26          |
| Rail                | $5.47    | 6.57            | 28          |
| Road                | $5.54    | 4.72            | 29          |
| Sea                 | $4.97    | 7.12            | 17          |

**Figure 1** (below) shows two key insights. The left panel demonstrates that Air transport has the highest average cost at $6.02, while Sea transport offers the lowest at $4.97. The right panel plots cost versus delivery time, revealing a critical finding: Road transport delivers the best value proposition with below-average costs ($5.54) and the fastest delivery time (4.72 days).

![Shipping Cost Analysis](../img/shipping_cost_analysis.png)

**Figure 2** (below) presents a heatmap of average shipping costs broken down by route and transportation mode combinations. This granular view exposes significant variation. For example, Route A with Sea transport costs only $3.81, while Route C with Sea transport costs $7.55—nearly double. Similarly, Air transport on Route A ($7.06) is substantially more expensive than Air on Routes B or C (~$5.25).

![Route Mode Heatmap](../img/route_mode_heatmap.png)

These visualizations directly support the dashboard's filtering capabilities. A supply chain manager can use these patterns to:
- Identify that Road transport offers optimal cost-time balance for time-sensitive shipments
- Recognize that Route A + Sea provides the most economical option when delivery time is flexible
- Flag Route C + Sea as a potential inefficiency requiring investigation (highest Sea cost)

The dashboard will enable users to dynamically filter by product type, route, and mode to replicate this analysis for their specific contexts, supporting data-driven decisions on carrier selection and route optimization.

The full analysis code is available in `notebooks/eda.ipynb`.

## Section 5: App Sketch & Description
Below is a sketch of what the dashboard could look like with a first draft of the metrics we want to include:

![Sketch](../img/sketch.png "App Sketch")

At a high level, the layout of the dashboard aims to provide a supply chain manager with key insights across the business. There are visualizations for a high level of how the business is doing overall (e.g. Map of route coverage across India, Defect rate per SKU and best sellers), as well as more intricate visualizations where actionable insights can be derived from. For example, a manager might see from the customer demographic visualization that there is a missed opportunity to market the fashion/beauty products to an untapped market. Filters have also been set for a few of the metric to allow for managers to drill down into the specifics of the root cause of an issue/missed opportunity.

The layout of the dashboard aims to keep the high-level summary visualizations together, and smaller, more detailed visualizations clustered together.
