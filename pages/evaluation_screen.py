import streamlit as st

st.title("Evaluation")
# Large text area
st.markdown("<h1 style='text-align: center;'>Final Score</h1>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="
        background-color:#90D5FF;
        border-radius:20px;
        padding:20px;
        height:200px;
        display:flex;
        justify-content:center;
        align-items:center;
        font-size:60px;
        text-align:center;
    ">
        {"<span font-weight:bold;> 6/10 </span>"}    
    </div>
    """,
    unsafe_allow_html=True
)

vert_space = '<div style="padding: 25px 5px;"></div>'
st.markdown(vert_space, unsafe_allow_html=True)
st.markdown(vert_space, unsafe_allow_html=True)

st.header("Finance")
st.markdown("""
    <style>
    .opaque-background1 {
        background-color: rgb(46, 46, 255, 0.2);  
        padding: 10px;
        border-radius: 20px;
    }
    .opaque-background1 p {
        color: #FFFFFF; 
        font-size: 16px;
    }
    </style>
    <div class="opaque-background1">
        <p>Finance Stuff.</p>
    </div>
""", unsafe_allow_html=True)


st.markdown(vert_space, unsafe_allow_html=True)

st.header("Growth Potential")
st.markdown("""
    <style>
    .opaque-background2 {
        background-color: rgb(92, 92, 255, 0.2);  
        padding: 10px;
        border-radius: 20px;
    }
    .opaque-background2 p {
        color: #FFFFFF; 
        font-size: 16px;
    }
    </style>
    <div class="opaque-background2">
        <p>Growth</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(vert_space, unsafe_allow_html=True)

st.header("Innovation")
st.markdown("""
    <style>
    .opaque-background3 {
        background-color: rgb(138, 138, 255, 0.2);  
        padding: 10px;
        border-radius: 20px;
    }
    .opaque-background3 p {
        color: #FFFFFF; 
        font-size: 16px;
    }
    </style>
    <div class="opaque-background3">
        <p>Innovating stuff</p>
    </div>
""", unsafe_allow_html=True)
