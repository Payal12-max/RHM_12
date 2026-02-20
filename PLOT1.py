from graphviz import Digraph

# Create Digraph object
dot = Digraph(comment='WESAD Pipeline', format='png')
dot.attr(rankdir='LR')  # Left to Right orientation

# Define node style
dot.attr('node', shape='box', style='rounded,filled', 
         fillcolor='#e1f5fe', color='#1565c0', fontname='Arial')

# Add Nodes
dot.node('A', 'WESAD Dataset\n(15 Subj, RespiBAN,\n700Hz)')
dot.node('B', 'Signal Filtering\n(EDA: Low-pass 5Hz\nBVP: Band-pass 0.5-8Hz)')
dot.node('C', 'Windowing\n(60s Window\n50% Overlap)')
dot.node('D', 'Feature Eng.\n(HRV, EDA Metrics)')
dot.node('E', 'Logistic Regression\n(Flattened Input)')
dot.node('F', 'LSTM Network\n(Sequential Input)')
dot.node('G', 'Evaluation\n(LOSO Validation)')

# Add Edges
dot.edge('A', 'B', label='Raw Signals')
dot.edge('B', 'C', label='Clean Signals')
dot.edge('C', 'D')
dot.edge('D', 'E')
dot.edge('D', 'F')
dot.edge('E', 'G')
dot.edge('F', 'G')

# Render
dot.render('wesad_pipeline', view=True)