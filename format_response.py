def replace_text(response):
    print("INSIDE REPLACE TEXT")
    response_text = response.split("<h4>")
    print("response_text",response_text)
    print("ype of response_text", type(response_text))
    for idx, resp in enumerate(response_text):
        print("IDX, resp", resp)
        if "about unilever:" in resp.lower():
            print("INSIDE IF")
            response_text[idx] = """<font color="blue">About Unilever:</font></h4>Be part of the world’s most successful, purpose-led business. Work with brands that are well-loved around the world, that improve the lives of our consumers and the communities around us. We promote innovation, big and small, to make our business win and grow; and we believe in business as a force for good. Unleash your curiosity, challenge ideas and disrupt processes; use your energy to make this happen. Our brilliant business leaders and colleagues provide mentorship and inspiration, so you can be at your best. Every day, nine out of ten Indian households use our products to feel good, look good and get more out of life – giving us a unique opportunity to build a brighter future."""    
        if "about uniops:" in resp.lower():
            print("INSIDE IF2")
            response_text[idx] = """<font color="blue">About UniOps:</font></h4>Unilever Operations (UniOps) is the global technology and operations engine of Unilever offering business services, technology, and enterprise solutions. UniOps serves over 190 locations and through a network of specialized service lines and partners delivers insights and innovations, user experiences and end-to-end seamless delivery making Unilever Purpose Led and Future Fit."""
            
    response_total = "<h4>".join(response_text)
    print("response_total", response_total)
    return response_total
            
            
